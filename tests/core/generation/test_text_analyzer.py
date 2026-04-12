import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from pathlib import Path

# 将项目根目录添加到 sys.path
project_root = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
sys.path.insert(0, str(project_root))

from core.workflow.video_summary.state import VideoSummaryState
from core.workflow.video_summary.nodes.text_analyzer import text_analyzer_node

class TestTextAnalyzerNode(unittest.TestCase):
    
    def setUp(self):
        """准备符合架构 State 的测试数据"""
        self.valid_state: VideoSummaryState = {
            "transcript": "Hello, this is a test video about AI and Architecture as Law.",
            "keyframes": [],
            "text_insights": "",
            "visual_insights": "",
            "draft_summary": "",
            "user_prompt": "Please focus on AI architecture.",
            "revision_count": 0,
            "feedback_instructions": "",
            "hallucination_score": "",
            "usefulness_score": ""
        }
        
    def test_empty_transcript(self):
        """边界情况 1：空或全为空格的 transcript，不应触发大模型调用"""
        state = self.valid_state.copy()
        state["transcript"] = "   "
        result = text_analyzer_node(state)
        self.assertEqual(result["text_insights"], "未提供有效的语音转录文本。")
        
    @patch.dict(os.environ, clear=True)
    def test_missing_api_key(self):
        """边界情况 2：缺少 API Key 时，必须抛出 ValueError，阻断后续无意义操作"""
        with self.assertRaisesRegex(ValueError, ".*OPENAI_API_KEY.*"):
            text_analyzer_node(self.valid_state)
            
    @patch.dict(os.environ, {"OPENAI_API_KEY": "fake_key_123", "OPENAI_BASE_URL": "https://fake.url"})
    @patch('core.workflow.video_summary.nodes.text_analyzer.OpenAI')
    def test_successful_analysis_no_tools(self, mock_openai_class):
        """一般情况：成功的 API 调用，模型未触发主动搜索，直接返回正常提炼结果"""
        # 准备 Mock
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices[0].message.tool_calls = None
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

    @patch.dict(os.environ, {"OPENAI_API_KEY": "fake_key_123", "OPENAI_BASE_URL": "https://fake.url"})
    @patch('core.workflow.video_summary.nodes.text_analyzer.OpenAI')
    @patch('core.workflow.video_summary.nodes.text_analyzer.execute_tavily_search')
    def test_tool_call_success_loop(self, mock_tavily_search, mock_openai_class):
        """核心创新情况：大模型主动发起 Tool Call 进行梗检索，并在下一轮返回最终结果"""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        # 第一次请求返回 Tool Call
        mock_tool_call = MagicMock()
        mock_tool_call.id = "call_123"
        mock_tool_call.function.name = "tavily_search"
        mock_tool_call.function.arguments = '{"query": "mhc meaning"}'
        
        mock_message_1 = MagicMock()
        mock_message_1.tool_calls = [mock_tool_call]
        mock_message_1.content = None
        
        mock_response_1 = MagicMock()
        mock_response_1.choices[0].message = mock_message_1
        
        # 第二次请求返回结合了检索知识的最终结果
        mock_message_2 = MagicMock()
        mock_message_2.tool_calls = None
        mock_message_2.content = "mhc 意思是..."
        
        mock_response_2 = MagicMock()
        mock_response_2.choices[0].message = mock_message_2
        
        # side_effect 模拟大模型的两次连续作答
        mock_client.chat.completions.create.side_effect = [mock_response_1, mock_response_2]
        
        # 拦截我们自己写的 Python 外部搜索函数
        mock_tavily_search.return_value = "mhc refers to Major Histocompatibility Complex..."
        
        result = text_analyzer_node(self.valid_state)
        
        # 断言系统自动拉起了 2 次大模型调用来完成 ReAct 闭环
        self.assertEqual(mock_client.chat.completions.create.call_count, 2)
        # 断言调用了搜网工具，并且传对了参数
        mock_tavily_search.assert_called_once_with("mhc meaning")
        # 断言输出包含大模型拿到工具结果后生成的最终内容
        self.assertEqual(result["text_insights"], "mhc 意思是...")

    @patch.dict(os.environ, {"OPENAI_API_KEY": "fake_key_123"})
    @patch('core.workflow.video_summary.nodes.text_analyzer.OpenAI')
    def test_tool_call_max_loop_fallback(self, mock_openai_class):
        """边界情况 4：防死循环。若大模型陷入疯狂 Tool Call，触发强制兜底退出"""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_tool_call = MagicMock()
        mock_tool_call.id = "call_123"
        mock_tool_call.function.name = "tavily_search"
        mock_tool_call.function.arguments = '{"query": "infinite loop"}'
        
        mock_message = MagicMock()
        mock_message.tool_calls = [mock_tool_call]
        mock_message.content = "这是我最后一次请求之前的废话"
        
        mock_response = MagicMock()
        mock_response.choices[0].message = mock_message
        
        # 始终返回 tool call
        mock_client.chat.completions.create.return_value = mock_response
        
        result = text_analyzer_node(self.valid_state)
        
        # text_analyzer 设定的 max_tool_calls 是 2
        self.assertEqual(mock_client.chat.completions.create.call_count, 2)
        self.assertEqual(result["text_insights"], "这是我最后一次请求之前的废话")

    @patch.dict(os.environ, {"OPENAI_API_KEY": "fake_key_123"})
    @patch('core.workflow.video_summary.nodes.text_analyzer.OpenAI')
    def test_api_error_handling(self, mock_openai_class):
        """边界情况 3：API 报错（如频率限制、网络超时），节点不能让整个工作流崩溃，而是记录异常信息"""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        # 模拟底层 SDK 抛出异常
        mock_client.chat.completions.create.side_effect = Exception("API Rate Limit Exceeded or Timeout")
        
        result = text_analyzer_node(self.valid_state)
        
        # 断言错误信息被正确捕获并按架构规范转化为 text_insights
        self.assertIn("[系统自动提示]：文本分析提取失败", result["text_insights"])
        self.assertIn("API Rate Limit Exceeded or Timeout", result["text_insights"])

if __name__ == '__main__':
    unittest.main()