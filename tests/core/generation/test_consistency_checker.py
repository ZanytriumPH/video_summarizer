import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from pathlib import Path

# 将项目根目录添加到 sys.path
project_root = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
sys.path.insert(0, str(project_root))

from core.workflow.video_summary.nodes.consistency_checker import consistency_checker_node

class TestConsistencyCheckerNode(unittest.TestCase):
    
    def setUp(self):
        """准备符合架构 State 的测试数据"""
        self.valid_state = {
            "draft_summary": "苹果发布了新款iPhone，搭载性能提升20%的A17芯片，采用了钛金属外壳。",
            "text_insights": "核心观点：苹果发布了新款 iPhone。金句：这是迄今为止最伟大的产品。",
            "visual_insights": "[00:15] PPT上显示了 A17 芯片的性能提升 20%。\n[00:30] 演讲者展示了钛金属外壳。",
            "user_prompt": "侧重芯片性能",
            "revision_count": 1,
            "critique": "" # 这是即将被更新的字段
        }

    def test_short_circuit_empty_draft(self):
        """边界情况 1：草稿为空时，直接短路放行（不消耗 Token）"""
        state = self.valid_state.copy()
        state["draft_summary"] = ""
        
        result = consistency_checker_node(state)
        self.assertEqual(result["critique"], "", "草稿为空应直接放行，返回空 critique")

    def test_short_circuit_max_revisions(self):
        """边界情况 2：达到或超过最大重写次数 (revision_count >= 2) 时，直接短路放行（防死循环）"""
        state = self.valid_state.copy()
        state["revision_count"] = 2
        
        result = consistency_checker_node(state)
        self.assertEqual(result["critique"], "", "重写次数达标应直接放行，返回空 critique")

    @patch.dict(os.environ, clear=True)
    def test_missing_api_key(self):
        """边界情况 3：缺少 API Key 时，抛出 ValueError 阻断无意义请求"""
        with self.assertRaisesRegex(ValueError, ".*OPENAI_API_KEY.*"):
            consistency_checker_node(self.valid_state)

    @patch.dict(os.environ, {"OPENAI_API_KEY": "fake_key_123", "OPENAI_BASE_URL": "https://fake.url"})
    @patch('core.workflow.video_summary.nodes.consistency_checker.OpenAI')
    def test_checker_approve(self, mock_openai_class):
        """一般情况 1：审查通过 (APPROVE)，无幻觉无遗漏"""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_response = MagicMock()
        
        # 模拟审查官认为草稿完美，返回大写的 APPROVE
        mock_response.choices[0].message.content = "APPROVE"
        mock_client.chat.completions.create.return_value = mock_response
        
        result = consistency_checker_node(self.valid_state)
        
        # 验证大模型调用
        mock_client.chat.completions.create.assert_called_once()
        # 重点：APPROVE 应该被转化为 "" 以便路由判定
        self.assertEqual(result["critique"], "", "APPROVE 应该转化为放行信号 (空字符串)")

    @patch.dict(os.environ, {"OPENAI_API_KEY": "fake_key_123", "OPENAI_BASE_URL": "https://fake.url"})
    @patch('core.workflow.video_summary.nodes.consistency_checker.OpenAI')
    def test_checker_reject_with_critique(self, mock_openai_class):
        """一般情况 2：审查驳回 (Needs Revision)，发现幻觉或遗漏"""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_response = MagicMock()
        
        # 模拟审查官发现问题
        fake_critique = "草稿中遗漏了听觉提炼里的金句：'这是迄今为止最伟大的产品。' 请加上。"
        mock_response.choices[0].message.content = fake_critique
        mock_client.chat.completions.create.return_value = mock_response
        
        result = consistency_checker_node(self.valid_state)
        
        self.assertEqual(result["critique"], fake_critique, "驳回时必须原样返回具体的修改意见")

    @patch.dict(os.environ, {"OPENAI_API_KEY": "fake_key_123"})
    @patch('core.workflow.video_summary.nodes.consistency_checker.OpenAI')
    def test_checker_api_error_fallback(self, mock_openai_class):
        """边界情况 4：审查官 API 调用异常时，降级处理为默认放行 (Approve)，防止状态机卡死"""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        # 模拟底层 SDK 抛出异常 (如网络中断、超时)
        mock_client.chat.completions.create.side_effect = Exception("API Server Timeout")
        
        result = consistency_checker_node(self.valid_state)
        
        # 断言系统发生异常时，安全降级为空字符串 (Approve)，保证流程走到 END
        self.assertEqual(result["critique"], "", "API 异常时应降级放行，返回空 critique")

if __name__ == '__main__':
    unittest.main()