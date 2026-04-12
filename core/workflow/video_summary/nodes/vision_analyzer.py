import os
from openai import OpenAI
from core.workflow.video_summary.state import VideoSummaryState

def vision_analyzer_node(state: VideoSummaryState) -> dict:
    """
    视觉处理节点。调用多模态大模型（Vision LLM），传入 keyframes 和对应的时间戳，
    要求模型描述画面中的关键动作、PPT 文本或场景变化。
    
    :param state: VideoSummaryState
    :return: dict 包含更新的 visual_insights 字段
    """
    keyframes = state.get("keyframes", [])
    user_prompt = state.get("user_prompt", "")
    
    if not keyframes:
        return {"visual_insights": "未提取到任何视频关键帧，无法进行视觉分析。"}

    # 1. 获取凭证 (依赖于 workflow_service.py 注入的环境变量)
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    
    if not api_key:
        raise ValueError("在执行视觉分析节点时，未能找到 OPENAI_API_KEY 环境变量。")
        
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    # 2. 构造极其严谨的系统提示词，严防“多模态幻觉”
    system_prompt = (
        "你是一个专业的多模态视频视觉分析专家。我将为你提供按时间顺序排列的视频关键帧截图。\n"
        "你的任务是：仔细观察每一帧画面，提取出对于理解视频内容至关重要的视觉信息。\n\n"
        "请重点关注以下三个维度：\n"
        "1. 📊 屏幕/PPT内容：提取画面中出现的关键文字、图表走势、标题。\n"
        "2. 🎬 动作与场景：描述人物的重要手势、演示动作、产品交互过程或场景的切换。\n"
        "3. ⏱️ 时间线串联：结合提供的时间戳，梳理视觉信息的发展脉络。\n\n"
        "【警告/约束】：\n"
        "- 保持绝对客观，【绝不能】凭空捏造（幻觉）画面中没有的内容。如果不确定，请直接忽略。\n"
        "- 输出格式必须清晰易读（推荐使用 Markdown 列表），并【必须】在每条结论前附上对应的时间戳（如 [00:15]）。"
    )
    
    # 3. 按照标准多模态格式组装消息体 (Text + Image URL Array)
    content_list = [
        {"type": "text", "text": f"【用户总结侧重点要求】：\n{user_prompt}\n\n以下是按时间顺序截取的视频关键帧："}
    ]
    
    for frame in keyframes:
        time_str = frame.get("time", "未知时间")
        base64_img = frame.get("image", "")
        
        if not base64_img:
            continue
            
        # 3.1 插入时间戳文本作为锚点
        content_list.append({
            "type": "text",
            "text": f"--- 当前画面时间戳: [{time_str}] ---"
        })
        
        # 3.2 插入 Base64 图片 (符合官方 Vision API 规范)
        content_list.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_img}",
                "detail": "auto" # 允许模型根据图片尺寸自动选择 high/low 策略
            }
        })
        
    print(f"  -> [Vision Analyzer Node] Calling Vision LLM API with {len(keyframes)} frames...")
    
    # 4. 执行多模态 API 调用
    try:
        # 支持通过环境变量单独指定视觉模型 (如 gemini-1.5-pro)，若未指定则退推至全局默认 (gpt-4o)
        model_name = os.getenv("OPENAI_VISION_MODEL_NAME", os.getenv("OPENAI_MODEL_NAME", "gpt-4o"))
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": content_list}
            ],
            temperature=0.2, # 极低的温度，强制视觉大模型保持客观“所见即所得”，避免发散发散思维
            max_tokens=2048  # 视觉信息量大，需提供足够的 token 空间
        )
        visual_insights = response.choices[0].message.content
        print("  -> [Vision Analyzer Node] Visual extraction successful.")
        return {"visual_insights": visual_insights}
    except Exception as e:
        print(f"  -> [Vision Analyzer Node] Error during Vision API call: {str(e)}")
        # 依然遵守异常吞并与上抛给 Review 节点的规范
        return {"visual_insights": f"[系统自动提示]：视觉分析提取失败，Vision LLM 调用异常：{str(e)}"}