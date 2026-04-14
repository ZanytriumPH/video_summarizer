from typing import Any, Dict, List
from langgraph.types import Send

from core.workflow.video_summary.state import VideoSummaryState


def map_dispatch_node(state: VideoSummaryState) -> Dict[str, Any]:
    """
    迭代 A：构建分发元信息，不改变现有主流程分析语义。
    """
    chunk_plan = state.get("chunk_plan", [])
    if not isinstance(chunk_plan, list):
        chunk_plan = []

    retry_count = state.get("chunk_retry_count", {})
    if not isinstance(retry_count, dict):
        retry_count = {}

    for chunk in chunk_plan:
        if not isinstance(chunk, dict):
            continue
        chunk_id = str(chunk.get("chunk_id", "")).strip()
        if not chunk_id:
            continue
        retry_count.setdefault(chunk_id, 0)

    reduce_debug_info = state.get("reduce_debug_info", {})
    if not isinstance(reduce_debug_info, dict):
        reduce_debug_info = {}

    reduce_debug_info.update(
        {
            "dispatch_ready": True,
            "chunk_count": len(chunk_plan),
            "dispatch_strategy": "send-api-dual-pilot"
            if str(state.get("concurrency_mode", "threadpool")).strip().lower() == "send_api"
            else "threadpool-node-parallel",
        }
    )

    return {
        "chunk_results": state.get("chunk_results", []),
        "chunk_retry_count": retry_count,
        "reduce_debug_info": reduce_debug_info,
    }


def synthesis_barrier_node(state: VideoSummaryState) -> Dict[str, Any]:
    """
    方案 A：中间汇聚门。
    - 不做业务计算，只透传并补充门控元信息
    - 用于表达“音视频分片结果已汇聚，准备进入 synthesis 二次分发”
    """
    reduce_debug_info = state.get("reduce_debug_info", {})
    if not isinstance(reduce_debug_info, dict):
        reduce_debug_info = {}

    chunk_plan = state.get("chunk_plan", [])
    if not isinstance(chunk_plan, list):
        chunk_plan = []
    total_chunks = len(chunk_plan)

    chunk_results = state.get("chunk_results", [])
    if not isinstance(chunk_results, list):
        chunk_results = []

    ready_chunk_ids = {
        str(item.get("chunk_id", "")).strip()
        for item in chunk_results
        if isinstance(item, dict)
        and str(item.get("chunk_id", "")).strip()
        and str(item.get("audio_insights", "")).strip()
        and str(item.get("vision_insights", "")).strip()
    }

    reduce_debug_info.update(
        {
            "synthesis_barrier_reached": True,
            "synthesis_ready_chunks": len(ready_chunk_ids),
            "synthesis_total_chunks": total_chunks,
            "synthesis_ready": total_chunks > 0 and len(ready_chunk_ids) == total_chunks,
        }
    )

    return {
        "chunk_results": chunk_results,
        "reduce_debug_info": reduce_debug_info,
    }


def route_audio_send_tasks(state: VideoSummaryState) -> List[Send]:
    """
    Send API 试点：仅对音频分支执行图级 fan-out。
    """
    concurrency_mode = str(state.get("concurrency_mode", "threadpool")).strip().lower()
    if concurrency_mode != "send_api":
        return []

    chunk_plan = state.get("chunk_plan", [])
    if not isinstance(chunk_plan, list):
        return []

    existing_results = state.get("chunk_results", [])
    existing_map: Dict[str, Dict[str, Any]] = {
        str(item.get("chunk_id", "")).strip(): dict(item)
        for item in existing_results
        if isinstance(item, dict) and str(item.get("chunk_id", "")).strip()
    }

    sends: List[Send] = []
    transcript = state.get("transcript", "")
    user_prompt = state.get("user_prompt", "")
    for chunk in chunk_plan:
        if not isinstance(chunk, dict):
            continue
        chunk_id = str(chunk.get("chunk_id", "")).strip()
        if not chunk_id:
            continue

        sends.append(
            Send(
                "chunk_audio_worker_node",
                {
                    "transcript": transcript,
                    "user_prompt": user_prompt,
                    "current_chunk": chunk,
                    "current_chunk_base_item": existing_map.get(chunk_id, {"chunk_id": chunk_id}),
                },
            )
        )

    return sends


def route_vision_send_tasks(state: VideoSummaryState) -> List[Send]:
    """
    Send API 试点：对视觉分支执行图级 fan-out。
    """
    concurrency_mode = str(state.get("concurrency_mode", "threadpool")).strip().lower()
    if concurrency_mode != "send_api":
        return []

    chunk_plan = state.get("chunk_plan", [])
    if not isinstance(chunk_plan, list):
        return []

    existing_results = state.get("chunk_results", [])
    existing_map: Dict[str, Dict[str, Any]] = {
        str(item.get("chunk_id", "")).strip(): dict(item)
        for item in existing_results
        if isinstance(item, dict) and str(item.get("chunk_id", "")).strip()
    }

    sends: List[Send] = []
    keyframes = state.get("keyframes", [])
    keyframes_base_path = str(state.get("keyframes_base_path", ""))
    user_prompt = state.get("user_prompt", "")
    for chunk in chunk_plan:
        if not isinstance(chunk, dict):
            continue
        chunk_id = str(chunk.get("chunk_id", "")).strip()
        if not chunk_id:
            continue

        sends.append(
            Send(
                "chunk_vision_worker_node",
                {
                    "keyframes": keyframes,
                    "keyframes_base_path": keyframes_base_path,
                    "user_prompt": user_prompt,
                    "current_chunk": chunk,
                    "current_chunk_base_item": existing_map.get(chunk_id, {"chunk_id": chunk_id}),
                },
            )
        )

    return sends


def route_synthesis_send_tasks(state: VideoSummaryState) -> List[Send]:
    """
    方案 A：二阶段 fan-out。
    仅在 send_api 模式下，且 audio/vision 所有 chunk 都整理完成后，才分发 synthesis 任务。
    """
    concurrency_mode = str(state.get("concurrency_mode", "threadpool")).strip().lower()
    if concurrency_mode != "send_api":
        return []

    chunk_plan = state.get("chunk_plan", [])
    if not isinstance(chunk_plan, list) or not chunk_plan:
        return []

    planned_chunk_ids: List[str] = []
    for chunk in chunk_plan:
        if not isinstance(chunk, dict):
            continue
        chunk_id = str(chunk.get("chunk_id", "")).strip()
        if chunk_id:
            planned_chunk_ids.append(chunk_id)

    if not planned_chunk_ids:
        return []

    chunk_results = state.get("chunk_results", [])
    if not isinstance(chunk_results, list):
        return []

    result_map: Dict[str, Dict[str, Any]] = {
        str(item.get("chunk_id", "")).strip(): dict(item)
        for item in chunk_results
        if isinstance(item, dict) and str(item.get("chunk_id", "")).strip()
    }

    # 触发时机保底：必须等待 audio_worker 和 vision_worker 整理完全部 chunk。
    all_ready = True
    for chunk_id in planned_chunk_ids:
        item = result_map.get(chunk_id, {})
        has_audio = bool(str(item.get("audio_insights", "")).strip())
        has_vision = bool(str(item.get("vision_insights", "")).strip())
        if not (has_audio and has_vision):
            all_ready = False
            break

    if not all_ready:
        return []

    sends: List[Send] = []
    user_prompt = str(state.get("user_prompt", ""))
    for chunk in chunk_plan:
        if not isinstance(chunk, dict):
            continue
        chunk_id = str(chunk.get("chunk_id", "")).strip()
        if not chunk_id:
            continue

        base_item = result_map.get(chunk_id, {"chunk_id": chunk_id})
        # 幂等：已生成 chunk_summary 的分片不重复派发
        if str(base_item.get("chunk_summary", "")).strip():
            continue
        if not str(base_item.get("audio_insights", "")).strip():
            continue
        if not str(base_item.get("vision_insights", "")).strip():
            continue

        sends.append(
            Send(
                "chunk_synthesizer_worker_node",
                {
                    "user_prompt": user_prompt,
                    "current_synthesis_chunk": chunk,
                    "current_synthesis_base_item": base_item,
                },
            )
        )

    return sends
