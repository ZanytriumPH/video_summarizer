
import os
from typing import IO

# 引入抽象层和具体策略
from core.extraction.base import VideoSource
from core.extraction.sources import UrlVideoSource, LocalFileVideoSource

# 不再需要导入 extractor 和 transcriber
from core.analysis.analyzer import ContentAnalyzer
from core.generation.report_generator import ReportGenerator
from utils.file_utils import clear_temp_folder

class VideoSummaryService:
    def __init__(self, api_key: str):
        # 从环境变量中获取 base_url
        self.base_url = os.getenv("OPENAI_BASE_URL")
        self.api_key = api_key
        
        # 核心组件初始化
        # 注意：现在只剩下 analyzer 和 generator
        self.analyzer = ContentAnalyzer(api_key, base_url=self.base_url)
        self.generator = ReportGenerator()

    def _process_source(self, source: VideoSource) -> str:
        """
        统一的内部处理逻辑：
        1. 使用 VideoSource 获取内容 (Transcript + Frames)
        2. 使用 Analyzer 分析内容
        """
        # 在开始前清理临时文件夹
        clear_temp_folder()

        try:
            # 1. 获取内容 (VideoSource 现在是完全独立的)
            transcript, frames = source.process()

            # 2. 分析
            print("Analyzing content...")
            summary = self.analyzer.analyze(transcript, frames)
            print("Analysis complete.")
            
            return summary
        finally:
            # 在结束后清理，确保不留垃圾文件
            clear_temp_folder()

    def process_video_from_url(self, url: str) -> str:
        """
        针对 URL 的完整流程。
        """
        # 创建 Source 实例时传入必要的配置
        source = UrlVideoSource(url, api_key=self.api_key, base_url=self.base_url)
        return self._process_source(source)

    def process_uploaded_video(self, uploaded_file: IO[bytes], original_filename: str) -> str:
        """
        针对上传文件的完整流程。
        """
        # 创建 Source 实例时传入必要的配置
        source = LocalFileVideoSource(
            uploaded_file, 
            original_filename, 
            api_key=self.api_key, 
            base_url=self.base_url
        )
        return self._process_source(source)
