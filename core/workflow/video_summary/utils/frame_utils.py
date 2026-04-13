import base64
from pathlib import Path
from typing import Any, Dict


def resolve_frame_image_base64(frame: Dict[str, Any], keyframes_base_path: str = "") -> str:
    """
    兼容读取关键帧图像：优先 image，缺失时尝试 frame_file。
    """
    inline_image = frame.get("image")
    if isinstance(inline_image, str) and inline_image.strip():
        return inline_image

    frame_file = frame.get("frame_file")
    if not isinstance(frame_file, str) or not frame_file.strip():
        return ""

    file_path = Path(frame_file)
    if not file_path.is_absolute() and keyframes_base_path:
        file_path = Path(keyframes_base_path) / file_path

    if not file_path.exists() or not file_path.is_file():
        return ""

    try:
        raw = file_path.read_bytes()
        if not raw:
            return ""
        return base64.b64encode(raw).decode("utf-8")
    except Exception:
        return ""