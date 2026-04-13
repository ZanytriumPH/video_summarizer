import unittest
from unittest.mock import patch

from core.workflow.api import summarize_video


class _FakeWorkflowApp:
    def stream(self, initial_state, config, stream_mode="updates"):
        yield {"chunk_planner_node": {"chunk_plan": [{"chunk_id": "chunk-001"}]}}
        yield {"fusion_drafter_node": {"draft_summary": "mock summary", "revision_count": 1}}


class TestMetricsLogging(unittest.TestCase):
    def test_metrics_events_are_emitted_when_enabled(self):
        with patch("core.workflow.api.create_checkpointer", return_value=object()):
            with patch("core.workflow.api.build_video_summary_graph", return_value=_FakeWorkflowApp()):
                with patch("core.workflow.api.ENABLE_METRICS_LOGGING", True):
                    with patch("core.workflow.api.METRICS_SAMPLE_RATE", 1.0):
                        with patch("core.workflow.api.log_metric_event") as mock_metric:
                            result = summarize_video(
                                transcript='{"segments": [{"start": 0, "end": 1, "text": "hello"}]}',
                                keyframes=[{"time": "00:00", "image": "x"}],
                                thread_id="thread-metrics",
                            )

        self.assertEqual(result, "mock summary")
        event_names = [call.args[1] for call in mock_metric.call_args_list]
        self.assertIn("workflow_started", event_names)
        self.assertIn("workflow_node_update", event_names)
        self.assertIn("workflow_finished", event_names)


if __name__ == "__main__":
    unittest.main()
