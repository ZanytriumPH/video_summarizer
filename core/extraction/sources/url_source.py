from pathlib import Path
from typing import Callable, Optional
from core.extraction.base import VideoSource
from core.extraction.infrastructure.video.downloader import VideoDownloader

class UrlVideoSource(VideoSource):
    """
    针对 URL 视频源的实现。
    使用 VideoDownloader 从网络下载视频。
    """
    def __init__(self, url: str, api_key: str, base_url: str = None):
        super().__init__(api_key, base_url)
        self.url = url
        self.downloader = VideoDownloader()

    def acquire_video(self, status_callback: Optional[Callable[[str], None]] = None) -> Path:
        """
        从 URL 下载视频。
        """
        if status_callback:
            status_callback(f"🌐 正在突破网络屏障，从远程服务器 {self.url[:30]}... 拉取原始视频流...")
        else:
            print(f"Downloading video from {self.url}...")
            
        return self.downloader.download(self.url)