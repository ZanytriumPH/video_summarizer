import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# 将项目根目录添加到 sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

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
    def test_successful_vision_analysis(self, mock_openai_class):
        """一般情况：成功的视觉多模态 API 调用，验证组装结构和返回值"""
        # 准备 Mock
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
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