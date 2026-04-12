import os
import streamlit as st
from dotenv import load_dotenv
from services.workflow_service import VideoSummaryService

# 在应用启动时尝试加载项目根目录的 .env 文件
load_dotenv()

def main():
    """
    Main entry point for the Streamlit Video Summarizer application.

    Sets up the page layout, sidebar inputs for API keys and video URLs,
    and handles the orchestration of video processing and summary display.
    """
    st.set_page_config(layout="wide")
    st.title("多模态智能视频总结 (Video Summarizer)")

    # Sidebar for inputs
    with st.sidebar:
        st.header("⚙️ Settings (配置)")
        
        # [前端 UX 优化] 自动读取环境变量作为输入框默认值，免除每次重启手填的烦恼
        default_api_key = os.getenv("OPENAI_API_KEY", "")
        default_base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        
        api_key = st.text_input("OpenAI API Key", value=default_api_key, type="password")
        base_url = st.text_input("OpenAI Base URL", value=default_base_url, help="如果您使用的是兼容 OpenAI 格式的中转 API，请在此修改地址。")
        
        # 选择视频来源
        source_type = st.radio("🎬 Video Source (视频来源)", ("YouTube URL", "Local Upload"))
        
        video_url = None
        uploaded_file = None

        if source_type == "YouTube URL":
            video_url = st.text_input("Video URL")
        else:
            uploaded_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi", "mkv"])

        st.markdown("---")
        st.header("🎯 Summary Requirements (总结偏好)")
        user_prompt = st.text_area(
            "您希望 AI 侧重总结什么内容？ (What would you like the AI to focus on?)", 
            placeholder="例如：请侧重于分析视频中产品演示的具体操作步骤和图表数据...",
            help="留空则会进行默认的全面综合总结。(Leave blank for a general comprehensive summary.)"
        )

        process_button = st.button("🚀 Generate Summary (开始总结)")

    # Main content area
    col1, col2 = st.columns(2)

    # 左侧显示视频
    with col1:
        st.header("📺 Video")
        if source_type == "YouTube URL" and video_url:
            st.video(video_url)
        elif source_type == "Local Upload" and uploaded_file:
            # Streamlit可以直接显示上传的文件对象
            st.video(uploaded_file)
        else:
            st.info("Please provide a video source to begin.")

    # 右侧显示摘要
    with col2:
        st.header("📝 Summary")
        
        if process_button:
            if not api_key:
                st.warning("Please enter your OpenAI API Key first.")
            elif source_type == "YouTube URL" and not video_url:
                st.warning("Please enter a valid YouTube URL.")
            elif source_type == "Local Upload" and not uploaded_file:
                st.warning("Please upload a video file.")
            else:
                summary = "" # 提前初始化以便在外部使用
                
                # [状态回传体验跃升] 使用 st.status 作为后台运行日志的容器
                with st.status("🔄 正在唤醒深度多模态解析引擎，请坐和放宽...", expanded=True) as status_container:
                    
                    # 声明一个闭包函数，它会被注入到庞大业务底座的最深处
                    def update_status_ui(msg: str):
                        status_container.update(label=msg)
                        # 在状态面板内部如极客流水线一般打出所有曾执行过的子任务日志
                        st.write(msg)

                    try:
                        service = VideoSummaryService(api_key=api_key, base_url=base_url)
                        
                        if source_type == "YouTube URL":
                            # 处理 URL
                            summary = service.process_video_from_url(
                                video_url, 
                                user_prompt=user_prompt, 
                                status_callback=update_status_ui
                            )
                        else:
                            # 处理上传的文件
                            summary = service.process_uploaded_video(
                                uploaded_file, 
                                uploaded_file.name, 
                                user_prompt=user_prompt, 
                                status_callback=update_status_ui
                            )
                        
                        status_container.update(
                            label="✅ 全链路执行完毕！所有的细节都逃不过多智能体网络的火眼金睛。", 
                            state="complete", 
                            expanded=False # 执行完毕后自动收起流水线日志，腾出屏幕空间
                        )
                        
                    except Exception as e:
                        status_container.update(label="❌ 系统异常，流水线熔断", state="error", expanded=True)
                        st.error(f"处理过程中发生严重异常: {e}")
                        
                # 【前端排版解耦】将最终的 Markdown 总结报告独立在外部主视觉区渲染
                if summary:
                    st.markdown(summary)
                    st.balloons() # 加入一点庆祝彩蛋
        else:
             st.markdown("Summary will appear here after processing...")

if __name__ == "__main__":
    main()