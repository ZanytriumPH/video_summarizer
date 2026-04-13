import unittest
from typing import cast

from core.workflow.video_summary.nodes.map_dispatcher import map_dispatch_node
from core.workflow.video_summary.state import VideoSummaryState


class TestMapDispatcherNode(unittest.TestCase):
    def test_map_dispatch_populates_retry_and_debug_info(self):
        chunk_results = [{"chunk_id": "chunk-000", "chunk_summary": "ok"}]
        state = cast(
            VideoSummaryState,
            {
                "chunk_plan": [
                    {"chunk_id": "chunk-000", "start_sec": 0, "end_sec": 120},
                    {"chunk_id": "chunk-001", "start_sec": 120, "end_sec": 240},
                ],
                "chunk_results": chunk_results,
                "chunk_retry_count": {"chunk-000": 3},
                "reduce_debug_info": {"trace_id": "trace-1"},
            },
        )

        result = map_dispatch_node(state)

        # 已有重试计数应保留，新分片补齐默认值
        self.assertEqual(result["chunk_retry_count"]["chunk-000"], 3)
        self.assertEqual(result["chunk_retry_count"]["chunk-001"], 0)
        self.assertTrue(result["reduce_debug_info"]["dispatch_ready"])
        self.assertEqual(result["reduce_debug_info"]["chunk_count"], 2)
        self.assertEqual(result["reduce_debug_info"]["dispatch_strategy"], "send-api-prepared")
        self.assertEqual(result["reduce_debug_info"]["trace_id"], "trace-1")
        # chunk_results 应原样透传
        self.assertIs(result["chunk_results"], chunk_results)

    def test_map_dispatch_handles_invalid_types(self):
        state = cast(
            VideoSummaryState,
            {
                "chunk_plan": "invalid",
                "chunk_retry_count": "invalid",
                "reduce_debug_info": "invalid",
                "chunk_results": "invalid-results",
            },
        )

        result = map_dispatch_node(state)
        self.assertEqual(result["chunk_retry_count"], {})
        self.assertEqual(result["reduce_debug_info"]["chunk_count"], 0)
        self.assertTrue(result["reduce_debug_info"]["dispatch_ready"])
        self.assertEqual(result["chunk_results"], "invalid-results")


if __name__ == "__main__":
    unittest.main()
