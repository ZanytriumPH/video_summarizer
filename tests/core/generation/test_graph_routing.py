import unittest

# [优化建议 3 落地] 引入类型提示，增强测试代码的上下文约束
from core.workflow.video_summary.state import VideoSummaryState

# [优化建议 1 落地] 引入全局常量，彻底消灭硬编码的魔法字符串
from core.workflow.video_summary.edges.router import (
    route_after_hallucination, 
    route_after_usefulness,
    ROUTE_HAS_HALLUCINATION,
    ROUTE_NO_HALLUCINATION,
    ROUTE_NOT_USEFUL,
    ROUTE_USEFUL
)

class TestGraphRouting(unittest.TestCase):
    
    def test_route_after_hallucination(self):
        """测试第一道防线：防幻觉路由 (Hallucination Grader -> Next Node)"""
        # 情况 1：存在幻觉 -> 打回重写 (Needs Revision)
        state_with_hallucination: VideoSummaryState = {"hallucination_score": "yes"} # type: ignore
        self.assertEqual(route_after_hallucination(state_with_hallucination), ROUTE_HAS_HALLUCINATION)
        
        # 情况 2：不存在幻觉 -> 放行到有用性审查 (Usefulness Grader)
        state_no_hallucination: VideoSummaryState = {"hallucination_score": "no"} # type: ignore
        self.assertEqual(route_after_hallucination(state_no_hallucination), ROUTE_NO_HALLUCINATION)
        
        # 情况 3：默认兜底 -> 若因异常未获取到字段 (键不存在)
        state_empty: VideoSummaryState = {} # type: ignore
        self.assertEqual(route_after_hallucination(state_empty), ROUTE_NO_HALLUCINATION, "字典中无该字段时应默认保守放行")
        
        # 情况 4：处理非规范的大小写 (如大模型偶尔输出 YES)
        state_upper: VideoSummaryState = {"hallucination_score": "YES"} # type: ignore
        self.assertEqual(route_after_hallucination(state_upper), ROUTE_HAS_HALLUCINATION, "应当对大小写脱敏")

    def test_route_after_hallucination_invalid_values(self):
        """边界情况 5：[优化建议 2 落地] 处理非法或意外的值，应当执行保守放行策略防死锁"""
        # 值为 None 的情况
        state_none: VideoSummaryState = {"hallucination_score": None} # type: ignore
        self.assertEqual(route_after_hallucination(state_none), ROUTE_NO_HALLUCINATION, "值为 None 时应当安全降级")
        
        # 值为无法解析的乱码或长句
        state_junk: VideoSummaryState = {"hallucination_score": "I am an AI, I don't know what you mean."} # type: ignore
        self.assertEqual(route_after_hallucination(state_junk), ROUTE_NO_HALLUCINATION, "无法解析的字符串应当安全降级")

    def test_route_after_usefulness(self):
        """测试第二道防线：防偏题路由 (Usefulness Grader -> Next Node)"""
        # 情况 1：偏离需求 -> 打回重写 (Needs Revision)
        state_not_useful: VideoSummaryState = {"usefulness_score": "no"} # type: ignore
        self.assertEqual(route_after_usefulness(state_not_useful), ROUTE_NOT_USEFUL)
        
        # 情况 2：满足需求 -> 放行至 END (大功告成)
        state_useful: VideoSummaryState = {"usefulness_score": "yes"} # type: ignore
        self.assertEqual(route_after_usefulness(state_useful), ROUTE_USEFUL)
        
        # 情况 3：默认兜底 -> 若因异常未获取到字段 (键不存在)
        state_empty: VideoSummaryState = {} # type: ignore
        self.assertEqual(route_after_usefulness(state_empty), ROUTE_USEFUL, "字典中无该字段时应默认保守放行")
        
        # 情况 4：处理非规范的大小写
        state_upper: VideoSummaryState = {"usefulness_score": "NO"} # type: ignore
        self.assertEqual(route_after_usefulness(state_upper), ROUTE_NOT_USEFUL, "应当对大小写脱敏")

    def test_route_after_usefulness_invalid_values(self):
        """边界情况 5：[优化建议 2 落地] 处理非法或意外的值，应当执行保守放行策略防死锁"""
        state_none: VideoSummaryState = {"usefulness_score": None} # type: ignore
        self.assertEqual(route_after_usefulness(state_none), ROUTE_USEFUL, "值为 None 时应当安全降级")
        
        state_junk: VideoSummaryState = {"usefulness_score": "This summary is okay but not perfect."} # type: ignore
        self.assertEqual(route_after_usefulness(state_junk), ROUTE_USEFUL, "无法解析的字符串应当安全降级")

if __name__ == '__main__':
    unittest.main()