import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# 将项目根目录添加到 sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from core.workflow.video_summary.nodes.text_analyzer import text_analyzer_node

class TestTextAnalyzerNode(unittest.TestCase):
    
    def setUp(self):
        """准备符合架构 State 的测试数据"""
        self.valid_state = {
            "transcript": "Hello, this is a test video about AI and Architecture as Law.",
            "user_prompt": "Please focus on AI architecture.",
        }
        
    def test_empty_transcript(self):
        """边界情况 1：空或全为空格的 transcript，不应触发大模型调用"""
        state = {"transcript": "   "}
        result = text_analyzer_node(state)
        self.assertEqual(result["text_insights"], "未提供有效的语音转录文本。")
        
    @patch.dict(os.environ, clear=True)
    def test_missing_api_key(self):
        """边界情况 2：缺少 API Key 时，必须抛出 ValueError，阻断后续无意义操作"""
        with self.assertRaisesRegex(ValueError, ".*OPENAI_API_KEY.*"):
            text_analyzer_node(self.valid_state)
            
    @patch.dict(os.environ, {"OPENAI_API_KEY": "fake_key_123", "OPENAI_BASE_URL": "https://fake.url"})
    @patch('core.workflow.video_summary.nodes.text_analyzer.OpenAI')
    def test_successful_analysis(self, mock_openai_class):
        """一般情况：成功的 API 调用，返回正常的提炼结果"""
        # 准备 Mock
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "1. 核心观点: AI 架构...\n2. 大纲: 介绍...\n3. 金句: 架构即法律。"
        mock_client.chat.completions.create.return_value = mock_response
        
        # 执行节点函数
        result = text_analyzer_node(self.valid_state)
        
        # 断言返回值
        self.assertEqual(result["text_insights"], "1. 核心观点: AI 架构...\n2. 大纲: 介绍...\n3. 金句: 架构即法律。")
        
        # 验证大模型是否被正确调用
        mock_client.chat.completions.create.assert_called_once()
        
        # 验证传入的 prompt 是否包含用户的要求和原文本
        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        messages = call_kwargs.get("messages", [])
        
        user_message = [msg["content"] for msg in messages if msg["role"] == "user"][0]
        self.assertIn("Hello, this is a test", user_message)
        self.assertIn("Please focus on AI architecture", user_message)

    @patch.dict(os.environ, {"OPENAI_API_KEY": "fake_key_123"})
    @patch('core.workflow.video_summary.nodes.text_analyzer.OpenAI')
    def test_api_error_handling(self, mock_openai_class):
        """边界情况 3：API 报错（如频率限制、网络超时），节点不能让整个工作流崩溃，而是记录异常信息"""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        # 模拟底层 SDK 抛出异常
        mock_client.chat.completions.create.side_effect = Exception("API Rate Limit Exceeded or Timeout")
        
        # 执行节点函数
        result = text_analyzer_node(self.valid_state)
        
        # 断言错误信息被正确捕获并按架构规范转化为 text_insights
        self.assertIn("[系统自动提示]：文本分析提取失败", result["text_insights"])
        self.assertIn("API Rate Limit Exceeded or Timeout", result["text_insights"])

if __name__ == '__main__':
    unittest.main()