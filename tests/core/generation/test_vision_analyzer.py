import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from pathlib import Path

# 将项目根目录添加到 sys.path
project_root = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
sys.path.insert(0, str(project_root))

from core.workflow.video_summary.nodes.vision_analyzer import vision_analyzer_node

class TestVisionAnalyzerNode(unittest.TestCase):
    
    def setUp(self):
        """准备符合架构 State 的测试数据"""
        self.valid_state = {
            "keyframes": [
                {"time": "00:00", "image": "base64_fake_data_1"},
                {"time": "00:15", "image": "base64_fake_data_2"}
            ],
            "user_prompt": "侧重看PPT",
        }
        
    def test_empty_keyframes(self):
        """边界情况 1：空的关键帧列表，不应触发多模态大模型调用"""
        state = {"keyframes": []}
        result = vision_analyzer_node(state)
        self.assertEqual(result["visual_insights"], "未提取到任何视频关键帧，无法进行视觉分析。")
        
    @patch.dict(os.environ, clear=True)
    def test_missing_api_key(self):
        """边界情况 2：缺少 API Key 时，必须抛出 ValueError"""
        with self.assertRaisesRegex(ValueError, ".*OPENAI_API_KEY.*"):
            vision_analyzer_node(self.valid_state)
            
    @patch.dict(os.environ, {"OPENAI_API_KEY": "fake_vision_key", "OPENAI_BASE_URL": "https://fake.url"})
    @patch('core.workflow.video_summary.nodes.vision_analyzer.OpenAI')
    def test_successful_vision_analysis_no_tools(self, mock_openai_class):
        """一般情况：成功的视觉多模态 API 调用，无触发工具，直接输出分析"""
        # 准备 Mock
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices[0].message.tool_calls = None
        mock_response.choices[0].message.content = "1. 动作: 挥手...\n2. PPT: AI 架构图。"
        mock_client.chat.completions.create.return_value = mock_response
        
        # 执行节点函数
        result = vision_analyzer_node(self.valid_state)
        
        # 断言返回值
        self.assertEqual(result["visual_insights"], "1. 动作: 挥手...\n2. PPT: AI 架构图。")
        
        # 验证大模型是否被正确调用
        mock_client.chat.completions.create.assert_called_once()
        
        # 验证传入的 messages 是否符合多模态的 List[Dict] 结构
        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        messages = call_kwargs.get("messages", [])
        
        # 找到 user 的内容 (必须是 list 而不是单纯的字符串)
        user_message_content = [msg["content"] for msg in messages if msg["role"] == "user"][0]
        self.assertIsInstance(user_message_content, list)
        
        # 验证长度：1 个系统前导文字 + 2*(1个时间锚点 + 1张图) = 5
        self.assertEqual(len(user_message_content), 5)
        
        # 验证第一项是否包含用户提示
        self.assertIn("侧重看PPT", user_message_content[0]["text"])
        
        # 验证图片类型和 Base64 的注入
        self.assertEqual(user_message_content[2]["type"], "image_url")
        self.assertIn("base64_fake_data_1", user_message_content[2]["image_url"]["url"])
        
        self.assertEqual(user_message_content[4]["type"], "image_url")
        self.assertIn("base64_fake_data_2", user_message_content[4]["image_url"]["url"])

    @patch.dict(os.environ, {"OPENAI_API_KEY": "fake_key_123", "OPENAI_BASE_URL": "https://fake.url"})
    @patch('core.workflow.video_summary.nodes.vision_analyzer.OpenAI')
    @patch('core.workflow.video_summary.nodes.vision_analyzer.execute_tavily_search')
    def test_tool_call_success_loop(self, mock_tavily_search, mock_openai_class):
        """核心创新情况：视觉大模型遇到盲点，主动发起“以图生文再搜索 (Tool Call)”，并在下一轮返回最终结果"""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        # 第一次请求：遭遇知识盲区，要求抛出 Tool Call
        mock_tool_call = MagicMock()
        mock_tool_call.id = "call_vision_123"
        mock_tool_call.function.name = "tavily_search"
        mock_tool_call.function.arguments = '{"query": "this is fine dog sitting in fire meme meaning"}'
        
        mock_message_1 = MagicMock()
        mock_message_1.tool_calls = [mock_tool_call]
        mock_message_1.content = None
        
        mock_response_1 = MagicMock()
        mock_response_1.choices[0].message = mock_message_1
        
        # 第二次请求：拿到 Python 提供给它的外部网页百科，终于恍然大悟输出结果
        mock_message_2 = MagicMock()
        mock_message_2.tool_calls = None
        mock_message_2.content = "这是一张著名的 This is fine 热门梗图，表示面对灾难强作镇定..."
        
        mock_response_2 = MagicMock()
        mock_response_2.choices[0].message = mock_message_2
        
        mock_client.chat.completions.create.side_effect = [mock_response_1, mock_response_2]
        
        # 拦截底层的网络调用
        mock_tavily_search.return_value = "This is fine is a meme of a dog sitting in a room on fire..."
        
        result = vision_analyzer_node(self.valid_state)
        
        # 严格断言 ReAct 流转次数（请求了 2 次 LLM）
        self.assertEqual(mock_client.chat.completions.create.call_count, 2)
        # 断言是否正确触发了以图生文的文本搜索
        mock_tavily_search.assert_called_once_with("this is fine dog sitting in fire meme meaning")
        # 验证输出了终态
        self.assertEqual(result["visual_insights"], "这是一张著名的 This is fine 热门梗图，表示面对灾难强作镇定...")

    @patch.dict(os.environ, {"OPENAI_API_KEY": "fake_key_123"})
    @patch('core.workflow.video_summary.nodes.vision_analyzer.OpenAI')
    def test_tool_call_max_loop_fallback(self, mock_openai_class):
        """边界情况 4：防死循环。视觉模型陷入无限次 Tool Call 循环，触发强制兜底退出"""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_tool_call = MagicMock()
        mock_tool_call.id = "call_vision_123"
        mock_tool_call.function.name = "tavily_search"
        mock_tool_call.function.arguments = '{"query": "infinite loop"}'
        
        mock_message = MagicMock()
        mock_message.tool_calls = [mock_tool_call]
        mock_message.content = "这是我最后一次请求之前的废话"
        
        mock_response = MagicMock()
        mock_response.choices[0].message = mock_message
        
        # 大模型像发疯一样始终返回 tool call
        mock_client.chat.completions.create.return_value = mock_response
        
        result = vision_analyzer_node(self.valid_state)
        
        # vision_analyzer 的 max_tool_calls 是 3，到达上限后直接断开
        self.assertEqual(mock_client.chat.completions.create.call_count, 3)
        self.assertEqual(result["visual_insights"], "这是我最后一次请求之前的废话", "由于强制短路，应当兜底输出它发疯前的最后一句有效回复")

    @patch.dict(os.environ, {"OPENAI_API_KEY": "fake_vision_key"})
    @patch('core.workflow.video_summary.nodes.vision_analyzer.OpenAI')
    def test_vision_api_error_handling(self, mock_openai_class):
        """边界情况 3：多模态 API 报错（如图片太大、Token 超限），异常被捕获且状态机不崩溃"""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        # 模拟底层 SDK 抛出异常
        mock_client.chat.completions.create.side_effect = Exception("Payload Too Large for Vision Model")
        
        # 执行节点函数
        result = vision_analyzer_node(self.valid_state)
        
        # 断言错误信息被正确捕获并返回
        self.assertIn("[系统自动提示]：视觉分析提取失败", result["visual_insights"])
        self.assertIn("Payload Too Large", result["visual_insights"])

if __name__ == '__main__':
    unittest.main()