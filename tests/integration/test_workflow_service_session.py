import unittest
from unittest.mock import patch

from services.workflow_service import VideoSummaryService


class TestWorkflowServiceSession(unittest.TestCase):
    def test_ask_at_timestamp_reuses_last_thread_id(self):
        """阶段4：服务层时间旅行追问应默认复用最近一次会话 thread_id。"""
        service = VideoSummaryService(api_key="fake-key")
        service.last_thread_id = "thread-from-summary"

        with patch("services.workflow_service.answer_question_at_timestamp", return_value="ok") as mock_answer:
            result = service.ask_at_timestamp(
                timestamp="00:10",
                question="这里讲了什么？",
            )

        self.assertEqual(result, "ok")
        self.assertEqual(mock_answer.call_args.kwargs["thread_id"], "thread-from-summary")


if __name__ == "__main__":
    unittest.main()