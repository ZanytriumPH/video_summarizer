
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import shutil
import os
import json

from core.extraction.infrastructure.transcriber import AudioTranscriber

class TestAudioTranscriber(unittest.TestCase):

    def setUp(self):
        """创建测试所需的临时目录和文件"""
        self.test_audio_dir = Path(__file__).parent / "test_temp_transcriber_audio"
        
        if self.test_audio_dir.exists():
            shutil.rmtree(self.test_audio_dir)
        self.test_audio_dir.mkdir()

        self.dummy_audio_path = self.test_audio_dir / "dummy_audio.mp3"
        self.dummy_audio_path.touch()

        self.api_key = "test_api_key_placeholder"

    def tearDown(self):
        """清理测试产生的临时目录"""
        if self.test_audio_dir.exists():
            shutil.rmtree(self.test_audio_dir)

    @patch('core.extraction.infrastructure.transcriber.openai.OpenAI')
    def test_transcribe(self, mock_openai_client):
        """测试 transcribe 方法"""
        # --- 准备模拟 ---
        mock_instance = MagicMock()
        mock_openai_client.return_value = mock_instance
        
        # 准备一个假的 TranscriptionVerbose 对象返回结果
        mock_transcript_obj = MagicMock()
        expected_json_string = '{\n  "text": "Hello, world.",\n  "language": "en"\n}'
        mock_transcript_obj.model_dump_json.return_value = expected_json_string
        
        mock_instance.audio.transcriptions.create.return_value = mock_transcript_obj

        # --- 执行测试 ---
        transcriber = AudioTranscriber(api_key=self.api_key)
        result = transcriber.transcribe(self.dummy_audio_path)

        # --- 断言 ---
        mock_openai_client.assert_called_once_with(api_key=self.api_key, base_url=None)
        mock_instance.audio.transcriptions.create.assert_called_once()
        
        _, kwargs = mock_instance.audio.transcriptions.create.call_args
        
        self.assertEqual(kwargs['model'], 'whisper-1')
        self.assertEqual(kwargs['response_format'], 'verbose_json')
        
        self.assertTrue(hasattr(kwargs['file'], 'read'))
        self.assertEqual(kwargs['file'].name, str(self.dummy_audio_path))

        # 验证返回的是否是预期的 JSON 字符串
        self.assertEqual(result, expected_json_string)

if __name__ == '__main__':
    unittest.main()
