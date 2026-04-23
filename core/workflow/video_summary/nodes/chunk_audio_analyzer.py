import json
import os
import re
import time
import threading
from typing import Any, Dict, List, Tuple

from openai import OpenAI

from config.settings import CHUNK_MAX_TOOL_CALLS, ENABLE_CHUNK_CACHE
from core.workflow.video_summary.state import VideoSummaryState
from core.workflow.video_summary.tools.search_tools import execute_tavily_search

_AUDIO_SEARCH_CACHE: Dict[str, str] = {}
_AUDIO_SEARCH_CACHE_LOCK = threading.Lock()


def _load_transcript_data(transcript: str) -> Dict[str, Any]:
    if not transcript or not transcript.strip():
        return {}
    try:
        data = json.loads(transcript)
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def _build_transcript_items(transcript_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    segments = transcript_data.get("segments", [])
    if isinstance(segments, list):
        for seg in segments:
            if isinstance(seg, dict):
                items.append(seg)

    chunks = transcript_data.get("chunks", [])
    if isinstance(chunks, list):
        for chunk in chunks:
            if isinstance(chunk, dict):
                items.append(chunk)

    return items


def _extract_chunk_text(transcript_items: List[Dict[str, Any]], indexes: List[int]) -> str:
    lines: List[str] = []
    for idx in indexes:
        if not isinstance(idx, int) or idx < 0 or idx >= len(transcript_items):
            continue
        text = str(transcript_items[idx].get("text", "")).strip()
        if text:
            lines.append(text)
    return "\n".join(lines)


def _candidate_queries(text: str, max_calls: int) -> List[str]:
    # 以大写缩写和驼峰词作为轻量候选，限制每个 chunk 的搜索次数
    acronyms = re.findall(r"\b[A-Z]{2,}\b", text)
    camel_words = re.findall(r"\b[A-Za-z]+[A-Z][A-Za-z]+\b", text)

    candidates: List[str] = []
    for token in acronyms + camel_words:
        if token not in candidates:
            candidates.append(token)
        if len(candidates) >= max_calls:
            break
    return candidates


def _search_with_cache(query: str) -> str:
    if ENABLE_CHUNK_CACHE:
        with _AUDIO_SEARCH_CACHE_LOCK:
            cached = _AUDIO_SEARCH_CACHE.get(query)
        if cached is not None:
            return cached

    result = execute_tavily_search(query)
    if ENABLE_CHUNK_CACHE:
        with _AUDIO_SEARCH_CACHE_LOCK:
            _AUDIO_SEARCH_CACHE[query] = result
    return result


def _llm_audio_chunk_summary(chunk_id: str, chunk_text: str, user_prompt: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    if not api_key:
        return f"[chunk={chunk_id}] 音频摘要（降级）:\n" + (chunk_text[:500] if chunk_text else "无可用语音证据")

    client = OpenAI(api_key=api_key, base_url=base_url)
    model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4o")
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": "你是分片音频分析助手。请对输入的转录片段做精炼摘要，输出要点与术语解释。",
            },
            {
                "role": "user",
                "content": f"[chunk_id]\n{chunk_id}\n\n[user_prompt]\n{user_prompt}\n\n[chunk_transcript]\n{chunk_text}",
            },
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""


def _process_single_chunk_audio(
    chunk_id: str,
    indexes: List[int],
    transcript_items: List[Dict[str, Any]],
    user_prompt: str,
) -> Tuple[str, Dict[str, Any]]:
    started = time.perf_counter()
    chunk_text = _extract_chunk_text(transcript_items, indexes)

    if not chunk_text:
        insights = f"[chunk={chunk_id}] 无可用 transcript 分片证据。"
        searches: List[Dict[str, str]] = []
    else:
        try:
            insights = _llm_audio_chunk_summary(chunk_id, chunk_text, user_prompt)
        except Exception as exc:
            insights = f"[chunk={chunk_id}] 音频分析降级：{str(exc)}\n\n{chunk_text[:400]}"

        searches = []
        for query in _candidate_queries(chunk_text, max(0, CHUNK_MAX_TOOL_CALLS)):
            searches.append({"query": query, "result": _search_with_cache(query)})

    latency_ms = int((time.perf_counter() - started) * 1000)

    delta = {
        "chunk_id": chunk_id,
        "audio_insights": insights,
        "evidence_refs": {
            "transcript_segment_indexes": indexes,
            "audio_searches": searches,
        },
        "token_usage": {
            "audio": 0,
        },
        "latency_ms": {
            "audio": latency_ms,
        },
    }
    return chunk_id, delta


def chunk_audio_worker_node(state: VideoSummaryState) -> dict:
    """
    Send API 路径下的单分片音频分析 worker。

    地位:
    - Send API 图级 fan-out 下的单分片执行单元。

    任务:
    - 仅读取 current_chunk 对应的 transcript 片段。
    - 生成单个 chunk 的 audio_insights。

    主要输入:
    - state["current_chunk"]
    - state["transcript"]
    - state["user_prompt"]

    主要输出:
    - chunk_results: 长度为 1 的列表，包含当前 chunk 的音频分析结果。
    """
    current_chunk = state.get("current_chunk", {})
    if not isinstance(current_chunk, dict):
        return {"chunk_results": []}

    chunk_id = str(current_chunk.get("chunk_id", "")).strip()
    if not chunk_id:
        return {"chunk_results": []}

    indexes = current_chunk.get("transcript_segment_indexes", [])
    if not isinstance(indexes, list):
        indexes = []

    transcript = str(state.get("transcript", ""))
    user_prompt = str(state.get("user_prompt", ""))
    transcript_items = _build_transcript_items(_load_transcript_data(transcript))

    _, merged = _process_single_chunk_audio(
        chunk_id,
        indexes,
        transcript_items,
        user_prompt,
    )
    return {"chunk_results": [merged]}
