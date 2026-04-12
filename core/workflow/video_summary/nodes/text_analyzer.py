import os
from openai import OpenAI
from core.workflow.video_summary.state import VideoSummaryState

def text_analyzer_node(state: VideoSummaryState) -> dict:
    """
    纯文本处理节点。负责读取 transcript，提取核心观点、章节主题和金句。这一步旨在过滤口语化的废话。
    
    :param state: VideoSummaryState
    :return: dict 包含更新的 text_insights 字段
    """
    transcript = state.get("transcript", "")
    user_prompt = state.get("user_prompt", "")
    
    if not transcript or not transcript.strip():
        return {"text_insights": "未提供有效的语音转录文本。"}

    # 1. 获取凭证 (严格遵循使用原生 SDK 的原则)
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    
    if not api_key:
        raise ValueError("在执行文本分析节点时，未能找到 OPENAI_API_KEY 环境变量。")
        
    # 2. 实例化原生 OpenAI 客户端
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    # 3. 构造严谨的 Prompt
    system_prompt = (
        "你是一位资深的视频内容分析专家。你的核心任务是：仔细阅读提供的视频语音识别文本（Transcript），"
        "过滤掉一切口语化的废话、语气词和无关紧要的过渡句，并在此基础上提取出高度结构化的核心信息。\n\n"
        "请务必输出以下三个维度的分析结果，并保持良好的 Markdown 结构：\n"
        "1. 🌟 核心观点 (Core Insights)：提炼视频想传达的最重要的 3-5 个观点。\n"
        "2. 📑 章节主题大纲 (Chapter Outlines)：按照逻辑流向，梳理视频的大纲骨架。\n"
        "3. 💡 关键金句提取 (Key Quotes)：摘录视频中最有洞察力或最具代表性的原话（如有）。"
    )
    
    user_content = f"【用户总结侧重点要求】\n{user_prompt}\n\n【视频语音识别完整文本】\n{transcript}"
    
    print("  -> [Text Analyzer Node] Calling LLM API for text insights extraction...")
    
    # 4. 执行 API 调用
    try:
        # 默认使用 gpt-4o，或允许通过环境变量覆盖
        model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4o")
        response = client.chat.completions.create(
            model=model_name, 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.3, # 较低的温度以保证分析结果的客观性与稳定性
        )
        insights = response.choices[0].message.content
        print("  -> [Text Analyzer Node] Extraction successful.")
        return {"text_insights": insights}
    except Exception as e:
        print(f"  -> [Text Analyzer Node] Error during API call: {str(e)}")
        # 遵循非功能性设计：吞掉会导致流程崩溃的异常，转化为文本记录，交由下游审查节点 (Reflector) 处理
        return {"text_insights": f"[系统自动提示]：文本分析提取失败，LLM 调用异常：{str(e)}"}