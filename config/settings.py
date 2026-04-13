
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
# 这会查找与此文件同级的 .env 文件，或者向上查找
# 我们将 .env 文件放在项目根目录
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)  # 从 .env 文件中加载环境变量（如 API 密钥）

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent  # 获取项目根目录的绝对路径

# 临时文件目录
TEMP_DIR = BASE_DIR / "temp"
TEMP_VIDEO_DIR = TEMP_DIR / "videos"
TEMP_AUDIO_DIR = TEMP_DIR / "audios"
TEMP_FRAMES_DIR = TEMP_DIR / "frames"

# 确保目录存在
for dir_path in [TEMP_VIDEO_DIR, TEMP_AUDIO_DIR, TEMP_FRAMES_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# 默认配置
DEFAULT_FRAME_INTERVAL = 2  # 默认每2秒抽一帧
MAX_IMAGE_SIZE = 768        # 图片长边限制

# 转文本模型配置
TRANSCRIBER_MODEL = os.getenv("TRANSCRIBER_MODEL", "whisper-1")  # 语音转文本模型

# Checkpoint 配置（5.2 第一阶段）
CHECKPOINT_BACKEND = os.getenv("CHECKPOINT_BACKEND", "memory")
CHECKPOINT_DB_URL = os.getenv("CHECKPOINT_DB_URL", "")

# 5.3 Map-Reduce（迭代 A）配置
MAP_CHUNK_SECONDS = int(os.getenv("MAP_CHUNK_SECONDS", "120"))
MAP_CHUNK_OVERLAP_SECONDS = int(os.getenv("MAP_CHUNK_OVERLAP_SECONDS", "10"))
MAP_MAX_PARALLELISM = int(os.getenv("MAP_MAX_PARALLELISM", "4"))

# 5.3 Map-Reduce（迭代 B）配置
CHUNK_MAX_TOOL_CALLS = int(os.getenv("CHUNK_MAX_TOOL_CALLS", "2"))
ENABLE_CHUNK_CACHE = os.getenv("ENABLE_CHUNK_CACHE", "true").strip().lower() in {"1", "true", "yes", "on"}

# 方案B阶段2：运行指标采样配置
ENABLE_METRICS_LOGGING = os.getenv("ENABLE_METRICS_LOGGING", "true").strip().lower() in {
    "1",
    "true",
    "yes",
    "on",
}
METRICS_SAMPLE_RATE = float(os.getenv("METRICS_SAMPLE_RATE", "1.0"))
if METRICS_SAMPLE_RATE < 0:
    METRICS_SAMPLE_RATE = 0.0
if METRICS_SAMPLE_RATE > 1:
    METRICS_SAMPLE_RATE = 1.0

# 方案B阶段3：keyframes 引用化 PoC 配置（默认关闭，保持兼容）
ENABLE_KEYFRAME_FILE_REFERENCE = os.getenv("ENABLE_KEYFRAME_FILE_REFERENCE", "false").strip().lower() in {
    "1",
    "true",
    "yes",
    "on",
}
KEYFRAME_REFERENCE_INCLUDE_INLINE_IMAGE = os.getenv(
    "KEYFRAME_REFERENCE_INCLUDE_INLINE_IMAGE", "false"
).strip().lower() in {"1", "true", "yes", "on"}
KEYFRAME_IMAGE_EXTENSION = os.getenv("KEYFRAME_IMAGE_EXTENSION", "jpg").strip().lower() or "jpg"

# 并发模式配置（方案B阶段1：内部开关，不暴露前端）
SUPPORTED_CONCURRENCY_MODES = {"threadpool", "send_api"}
CONCURRENCY_MODE = os.getenv("CONCURRENCY_MODE", "threadpool").strip().lower()
if CONCURRENCY_MODE not in SUPPORTED_CONCURRENCY_MODES:
    print(
        f"[settings] Invalid CONCURRENCY_MODE='{CONCURRENCY_MODE}', fallback to 'threadpool'."
    )
    CONCURRENCY_MODE = "threadpool"


def resolve_concurrency_mode(mode: str = "") -> str:
    """
    解析并规范化并发模式。
    - 传入空值时回退到全局配置 CONCURRENCY_MODE
    - 非法值统一降级为 threadpool
    """
    candidate = (mode or CONCURRENCY_MODE).strip().lower()
    if candidate in SUPPORTED_CONCURRENCY_MODES:
        return candidate
    return "threadpool"
