import os
import unittest
from unittest.mock import patch, MagicMock

from core.workflow.api import answer_question_at_timestamp


class _FakeCheckpointer:
    def __init__(self, checkpoint):
        self._checkpoint = checkpoint

    def get(self, _config):
        return self._checkpoint


class TestTimeTravelPipelineIntegration(unittest.TestCase):
    def test_answer_question_success_with_checkpoint_and_llm(self):
        """集成路径：checkpoint 命中 + LLM 可用时，应返回模型回答文本"""
        checkpoint = {
            "channel_values": {
                "transcript": '{"segments": [{"start": 9, "end": 13, "text": "target evidence"}]}',
                "keyframes": [
                    {"time": "00:08", "image": ""},
                    {"time": "00:12", "image": ""},
                ],
                "draft_summary": "历史总结草稿",
                "user_prompt": "请关注技术细节",
            }
        }

        with patch("core.workflow.api.create_checkpointer", return_value=_FakeCheckpointer(checkpoint)):
            with patch.dict(os.environ, {"OPENAI_API_KEY": "fake_key"}, clear=False):
                with patch("core.workflow.api.OpenAI") as mock_openai:
                    mock_client = MagicMock()
                    mock_resp = MagicMock()
                    mock_resp.choices = [MagicMock(message=MagicMock(content="这是追问回答"))]
                    mock_client.chat.completions.create.return_value = mock_resp
                    mock_openai.return_value = mock_client

                    result = answer_question_at_timestamp(
                        thread_id="thread-1",
                        timestamp="00:10",
                        question="这段在讲什么？",
                        window_seconds=10,
                    )

        self.assertEqual(result, "这是追问回答")

    def test_answer_question_thread_not_found(self):
        """集成路径：checkpoint 未命中时应返回可解释提示"""
        with patch("core.workflow.api.create_checkpointer", return_value=_FakeCheckpointer(None)):
            result = answer_question_at_timestamp(
                thread_id="missing-thread",
                timestamp="00:10",
                question="这段在讲什么？",
            )

        self.assertIn("未找到 thread_id=missing-thread", result)

    def test_answer_question_fallback_without_openai_key(self):
        """集成路径：无 OPENAI_API_KEY 时应走证据降级输出"""
        checkpoint = {
            "channel_values": {
                "transcript": '{"segments": [{"start": 30, "end": 35, "text": "window evidence"}]}',
                "keyframes": [{"time": "00:33", "image": ""}],
                "draft_summary": "历史草稿",
                "user_prompt": "请简洁",
            }
        }

        with patch("core.workflow.api.create_checkpointer", return_value=_FakeCheckpointer(checkpoint)):
            with patch.dict(os.environ, {}, clear=True):
                result = answer_question_at_timestamp(
                    thread_id="thread-2",
                    timestamp="00:32",
                    question="这个时间点的重点是什么？",
                )

        self.assertIn("[系统降级回答]", result)
        self.assertIn("目标时间戳: 00:32", result)
        self.assertIn("语音证据", result)

    def test_answer_question_invalid_arguments(self):
        """集成路径：非法参数应抛 ValueError，避免静默失败"""
        with self.assertRaises(ValueError):
            answer_question_at_timestamp(thread_id="", timestamp="00:10", question="q")

        with self.assertRaises(ValueError):
            answer_question_at_timestamp(thread_id="t1", timestamp="00:10", question="")

        with self.assertRaises(ValueError):
            answer_question_at_timestamp(thread_id="t1", timestamp="bad-ts", question="q")


if __name__ == "__main__":
    unittest.main()
