from pathlib import Path
from typing import IO, Callable, Optional
from core.extraction.base import VideoSource
from core.extraction.infrastructure.video.local_video_handler import LocalVideoHandler

class LocalFileVideoSource(VideoSource):
    """
    针对本地上传视频源的实现。
    使用 LocalVideoHandler 保存上传的文件。
    """
    def __init__(self, uploaded_file: IO[bytes], original_filename: str, api_key: str, base_url: str = None):
        super().__init__(api_key, base_url)
        self.uploaded_file = uploaded_file
        self.original_filename = original_filename
        self.handler = LocalVideoHandler()

    def acquire_video(self, status_callback: Optional[Callable[[str], None]] = None) -> Path:
        """
        保存上传的文件到临时目录。
        """
        if status_callback:
            status_callback(f"💾 正在将前端上传的文件 {self.original_filename} 灌入底层安全沙箱...")
        else:
            print(f"Saving uploaded file {self.original_filename}...")
            
        return self.handler.save_uploaded_file(self.uploaded_file, self.original_filename)