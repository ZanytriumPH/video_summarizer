
import unittest
import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

# 【修复】确保绝对可靠地加载根目录的 .env 文件
# 获取当前文件所在目录的父级父级父级... 到达项目根目录
project_root = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))
env_path = project_root / '.env'

if env_path.exists():
    print(f"Loading environment variables from: {env_path}")
    load_dotenv(dotenv_path=env_path, override=True)
else:
    print(f"[WARNING] .env file not found at {env_path}. Falling back to default env variables.")
    load_dotenv()

try:
    from core.extraction.sources.local_source import LocalFileVideoSource
except ImportError:
    import sys
    sys.path.insert(0, str(project_root))
    from core.extraction.sources.local_source import LocalFileVideoSource

# 【重要】请修改此路径为您本机实际存在的视频文件路径
TEST_VIDEO_PATH = Path(r"C:\Users\rbxu3\Downloads\偶尔小头控制大头可以理解、长期被控制就有问题.mp4")

class TestLocalSourceIntegration(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """设置测试环境"""
        # 1. 检查 API Key
        cls.api_key = os.getenv("OPENAI_API_KEY")
        cls.base_url = os.getenv("OPENAI_BASE_URL")
        
        print(f"Debug - Base URL loaded: {cls.base_url}")
        
        if not cls.api_key:
            raise unittest.SkipTest("OPENAI_API_KEY not found in environment variables. Skipping integration test.")
        
        # 2. 检查测试视频文件
        if not TEST_VIDEO_PATH.exists():
             print(f"Warning: Test video not found at {TEST_VIDEO_PATH}. Skipping test.")
             raise unittest.SkipTest(f"Test video file not found at {TEST_VIDEO_PATH}")

        # 3. 创建唯一的输出目录
        test_name = Path(__file__).stem  # e.g., "test_local_source_integration"
        cls.output_dir = project_root / "test_output" / test_name
        
        if cls.output_dir.exists():
            shutil.rmtree(cls.output_dir)
        cls.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Test outputs will be saved to: {cls.output_dir.resolve()}")

    def test_process_local_video(self):
        """测试 LocalFileVideoSource 处理真实视频并保存结果"""
        print(f"Testing with video: {TEST_VIDEO_PATH}")
        
        with open(TEST_VIDEO_PATH, "rb") as video_file:
            source = LocalFileVideoSource(
                uploaded_file=video_file,
                original_filename=TEST_VIDEO_PATH.name,
                api_key=self.api_key,
                base_url=self.base_url
            )
            
            print("Starting processing... this may take a while.")
            transcript, frames = source.process()
            
            # --- 保存结果 ---
            transcript_path = self.output_dir / "transcript.txt"
            with open(transcript_path, "w", encoding="utf-8") as f:
                f.write(transcript)
            print(f"Transcript saved to {transcript_path}")
            
            import base64
            frames_dir = self.output_dir / "frames"
            frames_dir.mkdir(exist_ok=True)
            
            for i, frame_b64 in enumerate(frames):
                try:
                    frame_data = base64.b64decode(frame_b64)
                    frame_path = frames_dir / f"frame_{i:03d}.jpg"
                    with open(frame_path, "wb") as f:
                        f.write(frame_data)
                except Exception as e:
                    print(f"Failed to save frame {i}: {e}")

            print(f"Saved {len(frames)} frames to {frames_dir}")
            
            # --- 断言 ---
            self.assertTrue(len(transcript) > 0, "Transcript should not be empty")
            self.assertTrue(len(frames) > 0, "Should extract at least one frame")

if __name__ == '__main__':
    unittest.main()
