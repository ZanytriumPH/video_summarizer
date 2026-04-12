from typing import Literal
from core.workflow.video_summary.state import VideoSummaryState

# [消除魔法字符串]：将图路由的信号提炼为全局防腐常量
ROUTE_HAS_HALLUCINATION = "Has Hallucination"
ROUTE_NO_HALLUCINATION = "No Hallucination"
ROUTE_NOT_USEFUL = "Not Useful"
ROUTE_USEFUL = "Useful"

def route_after_hallucination(state: VideoSummaryState) -> Literal["Has Hallucination", "No Hallucination"]: # type: ignore
    """
    [Self-RAG 第一道防线路由]：
    根据幻觉评分器 (hallucination_grader) 的输出决定流向。
    若存在幻觉 -> 回流起草节点重写 (Needs Revision)。
    若无幻觉 -> 流向下一道防线：有用性评分器。
    
    :param state: VideoSummaryState
    :return: 下一步路由指令
    """
    score = state.get("hallucination_score")
    
    # [健壮性增强]：处理 None、非字符串类型等非法值，保守放行以防止系统死锁
    if not score or not isinstance(score, str):
        return ROUTE_NO_HALLUCINATION
        
    score = score.lower()
    if score == "yes":
        return ROUTE_HAS_HALLUCINATION
    else:
        return ROUTE_NO_HALLUCINATION


def route_after_usefulness(state: VideoSummaryState) -> Literal["Not Useful", "Useful"]: # type: ignore
    """
    [Self-RAG 第二道防线路由]：
    根据有用性评分器 (usefulness_grader) 的输出决定流向。
    若偏离需求 -> 回流起草节点重写 (Needs Revision)。
    若满足需求 -> 大功告成，流向终点 END。
    
    :param state: VideoSummaryState
    :return: 下一步路由指令
    """
    score = state.get("usefulness_score")
    
    # [健壮性增强]：处理 None、非字符串类型等非法值，保守放行以防死锁
    if not score or not isinstance(score, str):
        return ROUTE_USEFUL
        
    score = score.lower()
    if score == "no":
        return ROUTE_NOT_USEFUL
    else:
        return ROUTE_USEFUL