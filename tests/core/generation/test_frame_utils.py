import base64
import unittest
from pathlib import Path

from core.workflow.video_summary.utils.frame_utils import resolve_frame_image_base64


class TestFrameTools(unittest.TestCase):
    def test_resolve_inline_image_first(self):
        frame = {"time": "00:01", "image": "inline_data", "frame_file": "x.jpg"}
        self.assertEqual(resolve_frame_image_base64(frame, ""), "inline_data")

    def test_resolve_image_from_frame_file(self):
        temp_dir = Path("./test_temp_frames")
        temp_dir.mkdir(parents=True, exist_ok=True)
        try:
            target = temp_dir / "a.jpg"
            raw = b"abc123"
            target.write_bytes(raw)

            frame = {"time": "00:02", "frame_file": "a.jpg"}
            resolved = resolve_frame_image_base64(frame, str(temp_dir))
            self.assertEqual(resolved, base64.b64encode(raw).decode("utf-8"))
        finally:
            for child in temp_dir.iterdir():
                child.unlink()
            temp_dir.rmdir()


if __name__ == "__main__":
    unittest.main()