import json
from typing import Dict, List, Optional, Tuple


def parse_timestamp_to_seconds(timestamp: str) -> int:
    """
    支持 MM:SS 或 HH:MM:SS，返回总秒数。
    """
    if not timestamp or not timestamp.strip():
        raise ValueError("timestamp is required")

    parts = timestamp.strip().split(":")
    if len(parts) == 2:
        mm, ss = parts
        return int(mm) * 60 + int(ss)
    if len(parts) == 3:
        hh, mm, ss = parts
        return int(hh) * 3600 + int(mm) * 60 + int(ss)

    raise ValueError(f"Unsupported timestamp format: {timestamp}")


def format_seconds(total_seconds: float) -> str:
    """
    将秒数格式化为 HH:MM:SS。
    """
    seconds = max(0, int(total_seconds))
    hh = seconds // 3600
    mm = (seconds % 3600) // 60
    ss = seconds % 60
    return f"{hh:02d}:{mm:02d}:{ss:02d}"


def find_nearest_keyframe(keyframes: List[Dict], target_seconds: int) -> Optional[Dict]:
    """
    按时间戳找最近邻关键帧。
    """
    if not keyframes:
        return None

    nearest: Optional[Dict] = None
    min_delta = 10**9

    for frame in keyframes:
        frame_time = frame.get("time", "")
        try:
            frame_seconds = parse_timestamp_to_seconds(str(frame_time))
        except Exception:
            continue

        delta = abs(frame_seconds - target_seconds)
        if delta < min_delta:
            min_delta = delta
            nearest = frame

    return nearest


def extract_transcript_window(transcript: str, target_seconds: int, window_seconds: int = 20) -> str:
    """
    从 Whisper verbose_json 字符串中抽取目标时间窗的文本证据。
    """
    if not transcript or not transcript.strip():
        return "[无音频转录可用]"

    try:
        data = json.loads(transcript)
    except Exception:
        # 非 JSON 场景：按普通文本降级
        return transcript[:1200]

    segments = data.get("segments", []) if isinstance(data, dict) else []
    if not isinstance(segments, list) or not segments:
        # Whisper 某些返回可能只有 text 字段
        text = data.get("text", "") if isinstance(data, dict) else ""
        return text[:1200] if text else "[无可用转录分段]"

    left = max(0, target_seconds - max(0, window_seconds))
    right = target_seconds + max(0, window_seconds)
    lines: List[str] = []

    for seg in segments:
        if not isinstance(seg, dict):
            continue
        try:
            start = float(seg.get("start", 0))
            end = float(seg.get("end", start))
        except Exception:
            continue

        # 时间窗重叠判定
        if end < left or start > right:
            continue

        text = str(seg.get("text", "")).strip()
        if not text:
            continue

        lines.append(f"[{format_seconds(start)}-{format_seconds(end)}] {text}")

    if not lines:
        return "[该时间窗未命中可用语音分段]"

    return "\n".join(lines)
