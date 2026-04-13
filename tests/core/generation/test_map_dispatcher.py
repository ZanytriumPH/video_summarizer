import unittest
from typing import cast

from core.workflow.video_summary.nodes.map_dispatcher import build_chunk_sends, map_dispatch_node
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

    def test_build_chunk_sends_precise_payload_and_filtering(self):
        chunk_0 = {"chunk_id": "chunk-000", "start_sec": 0, "end_sec": 120}
        chunk_1 = {"chunk_id": "chunk-001", "start_sec": 120, "end_sec": 240}

        state = cast(
            VideoSummaryState,
            {
                "chunk_plan": [
                    chunk_0,
                    "not-a-dict",
                    {"start_sec": 240, "end_sec": 360},
                    {"chunk_id": "   ", "start_sec": 360, "end_sec": 480},
                    chunk_1,
                ]
            },
        )

        sends = build_chunk_sends(state, target_node="chunk_worker_node")
        self.assertEqual(len(sends), 2)
        self.assertEqual(sends[0].node, "chunk_worker_node")
        self.assertEqual(sends[1].node, "chunk_worker_node")
        self.assertEqual(sends[0].arg["chunk_id"], "chunk-000")
        self.assertEqual(sends[1].arg["chunk_id"], "chunk-001")
        self.assertEqual(sends[0].arg["current_chunk"], chunk_0)
        self.assertEqual(sends[1].arg["current_chunk"], chunk_1)

    def test_build_chunk_sends_handles_non_list_chunk_plan(self):
        state = cast(VideoSummaryState, {"chunk_plan": "invalid"})
        sends = build_chunk_sends(state, target_node="chunk_worker_node")
        self.assertEqual(sends, [])

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
