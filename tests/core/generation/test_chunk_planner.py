import unittest
from unittest.mock import patch
from typing import cast

from core.workflow.video_summary.planner.chunk_planner import chunk_planner_node
from core.workflow.video_summary.state import VideoSummaryState


class TestChunkPlannerNode(unittest.TestCase):
    def test_builds_chunk_plan_from_transcript_and_keyframes(self):
        state = {
            "transcript": '{"segments": [{"start": 0, "end": 35, "text": "a"}, {"start": 40, "end": 140, "text": "b"}]}',
            "keyframes": [
                {"time": "00:10", "image": "x"},
                {"time": "01:10", "image": "y"},
                {"time": "02:10", "image": "z"},
            ],
        }

        with patch("core.workflow.video_summary.planner.chunk_planner.MAP_CHUNK_SECONDS", 60):
            result = chunk_planner_node(state)  # type: ignore

        self.assertIn("video_duration_seconds", result)
        self.assertIn("chunk_plan", result)
        self.assertEqual(result["video_duration_seconds"], 140)
        self.assertTrue(result["chunk_plan"])
        self.assertEqual(len(result["chunk_plan"]), 3)

        first_chunk = result["chunk_plan"][0]
        self.assertEqual(first_chunk["chunk_id"], "chunk-000")
        self.assertGreaterEqual(first_chunk["end_sec"], first_chunk["start_sec"])
        self.assertIn("keyframe_indexes", first_chunk)
        self.assertIn("transcript_segment_indexes", first_chunk)
        self.assertEqual(first_chunk["start_sec"], 0)
        self.assertEqual(first_chunk["end_sec"], 60)
        self.assertEqual(first_chunk["keyframe_indexes"], [0])
        self.assertEqual(first_chunk["transcript_segment_indexes"], [0, 1])

        second_chunk = result["chunk_plan"][1]
        self.assertEqual(second_chunk["chunk_id"], "chunk-001")
        self.assertEqual(second_chunk["start_sec"], 60)
        self.assertEqual(second_chunk["end_sec"], 120)
        self.assertEqual(second_chunk["keyframe_indexes"], [1])
        self.assertEqual(second_chunk["transcript_segment_indexes"], [1])

        third_chunk = result["chunk_plan"][2]
        self.assertEqual(third_chunk["chunk_id"], "chunk-002")
        self.assertEqual(third_chunk["start_sec"], 120)
        self.assertEqual(third_chunk["end_sec"], 140)
        self.assertEqual(third_chunk["keyframe_indexes"], [2])
        self.assertEqual(third_chunk["transcript_segment_indexes"], [1])

    def test_fallback_for_empty_inputs(self):
        result = chunk_planner_node({"transcript": "", "keyframes": []})  # type: ignore
        self.assertEqual(result["video_duration_seconds"], 0)
        self.assertEqual(len(result["chunk_plan"]), 1)
        self.assertEqual(result["chunk_plan"][0]["start_sec"], 0)
        self.assertEqual(result["chunk_plan"][0]["end_sec"], 0)

    def test_handles_malformed_transcript_json(self):
        state = cast(
            VideoSummaryState,
            {
                "transcript": "{bad-json}",
                "keyframes": [{"time": "00:05", "image": "x"}],
            },
        )

        with patch("core.workflow.video_summary.planner.chunk_planner.MAP_CHUNK_SECONDS", 60):
            result = chunk_planner_node(state)

        self.assertEqual(result["video_duration_seconds"], 5)
        self.assertEqual(len(result["chunk_plan"]), 1)
        self.assertEqual(result["chunk_plan"][0]["keyframe_indexes"], [0])
        self.assertEqual(result["chunk_plan"][0]["transcript_segment_indexes"], [])

    def test_ignores_keyframes_without_time(self):
        state = cast(
            VideoSummaryState,
            {
                "transcript": '{"segments": [{"start": 0, "end": 10, "text": "a"}]}',
                "keyframes": [
                    {"image": "missing-time"},
                    {"time": "00:08", "image": "ok"},
                ],
            },
        )

        with patch("core.workflow.video_summary.planner.chunk_planner.MAP_CHUNK_SECONDS", 60):
            result = chunk_planner_node(state)

        self.assertEqual(result["video_duration_seconds"], 10)
        self.assertEqual(len(result["chunk_plan"]), 1)
        self.assertEqual(result["chunk_plan"][0]["keyframe_indexes"], [1])

    def test_uses_duration_field_when_segments_missing(self):
        state = cast(
            VideoSummaryState,
            {
                "transcript": '{"text": "hello", "language": "en", "duration": 95.4}',
                "keyframes": [],
            },
        )

        with patch("core.workflow.video_summary.planner.chunk_planner.MAP_CHUNK_SECONDS", 60):
            result = chunk_planner_node(state)

        self.assertEqual(result["video_duration_seconds"], 95)
        self.assertEqual(len(result["chunk_plan"]), 2)
        self.assertEqual(result["chunk_plan"][0]["start_sec"], 0)
        self.assertEqual(result["chunk_plan"][0]["end_sec"], 60)
        self.assertEqual(result["chunk_plan"][1]["start_sec"], 60)
        self.assertEqual(result["chunk_plan"][1]["end_sec"], 95)

    def test_supports_chunks_timestamp_format(self):
        state = cast(
            VideoSummaryState,
            {
                "transcript": (
                    '{"chunks": ['
                    '{"timestamp": [0, 12], "text": "a"}, '
                    '{"timestamp": [65, 78], "text": "b"}'
                    '], "duration": 80}'
                ),
                "keyframes": [{"time": "00:05", "image": "x"}],
            },
        )

        with patch("core.workflow.video_summary.planner.chunk_planner.MAP_CHUNK_SECONDS", 60):
            result = chunk_planner_node(state)

        self.assertEqual(result["video_duration_seconds"], 80)
        self.assertEqual(len(result["chunk_plan"]), 2)
        self.assertEqual(result["chunk_plan"][0]["transcript_segment_indexes"], [0])
        self.assertEqual(result["chunk_plan"][1]["transcript_segment_indexes"], [1])


if __name__ == "__main__":
    unittest.main()
