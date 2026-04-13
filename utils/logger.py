
import logging
import sys
import json
from typing import Any

def setup_logger(name: str = "video_summarizer", level: int = logging.INFO) -> logging.Logger:
    """
    配置并返回一个日志记录器
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def log_metric_event(logger: logging.Logger, event: str, **fields: Any) -> None:
    """
    统一输出结构化指标事件，便于后续检索与对比。
    """
    payload = {
        "event": event,
        "fields": fields,
    }
    logger.info("METRIC %s", json.dumps(payload, ensure_ascii=False, sort_keys=True))
