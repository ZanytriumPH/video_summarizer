from typing import Any, Dict, List

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
            "dispatch_strategy": "send-api-prepared",
        }
    )

    return {
        "chunk_results": state.get("chunk_results", []),
        "chunk_retry_count": retry_count,
        "reduce_debug_info": reduce_debug_info,
    }
