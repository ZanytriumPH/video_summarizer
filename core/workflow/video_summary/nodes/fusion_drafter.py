import os
from openai import OpenAI
from core.workflow.video_summary.state import VideoSummaryState

def fusion_drafter_node(state: VideoSummaryState) -> dict:
    """
    核心的“成文节点” (Drafter)。
    接收上游聚合节点输出的 aggregated_chunk_insights，
    负责将结构化证据整理为最终高质量总结。
    [Self-RAG 升级]: 如果存在反馈意见 (feedback_instructions)，则必须结合修改意见重新生成修正版草稿。
    
    :param state: VideoSummaryState
    :return: dict 包含更新的 draft_summary 和增加的 revision_count
    """
    current_count = state.get("revision_count", 0)
    aggregated_chunk_insights = state.get("aggregated_chunk_insights", "")
    user_prompt = state.get("user_prompt", "")
    feedback_instructions = state.get("feedback_instructions", "")

    # 1. 获取环境变量凭证
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    
    if not api_key:
        raise ValueError("在执行融合组装节点时，未能找到 OPENAI_API_KEY 环境变量。")
        
    client = OpenAI(api_key=api_key, base_url=base_url)

    # 2. 构造 System Prompt（聚合输入 -> 最终成文）
    system_prompt = (
        "你是一个顶级的视频内容编辑与深度报告撰写专家。\n"
        "你的输入是按时间片聚合后的多模态证据（Chunk Aggregated Insights）。"
        "你的任务是基于这些证据生成一份高质量、连贯且逻辑自洽的视频总结报告。\n\n"
        "【架构级约束指令】：\n"
        "1. 🔗 证据优先：仅允许使用输入证据中的信息，不得补造事实。\n"
        "2. 🧭 时间一致性：尽量保持时间线顺序与逻辑衔接，必要时指出跨片段关联。\n"
        "3. 📝 专业排版规范：输出必须使用易于阅读的 Markdown 语法。建议包含：【内容导读】、【核心内容解析】、【关键结论】、【总结与建议】等模块。"
    )

    # 3. [Self-RAG 升级] 双重评分机制介入
    if feedback_instructions and feedback_instructions.strip():
        system_prompt += (
            f"\n\n⚠️ 【重要警告：这是第 {current_count + 1} 次重写草稿】\n"
            "在上一版的草稿中，双重质量评分器 (Grader) 指出了以下的幻觉捏造或偏题问题。请务必在本次生成中严格遵照以下修改指令进行定点切除与修正：\n"
            f"====== 强制修改指令 (Feedback Instructions) ======\n"
            f"{feedback_instructions}\n"
            f"=================================================="
        )

    # 4. 组装 User Content
    user_content = (
        f"【用户期望的总结侧重点】：\n{user_prompt}\n\n"
        f"【分片聚合证据（唯一输入）】：\n{aggregated_chunk_insights}"
    )

    print(f"  -> [Fusion Drafter Node] Drafting final report from aggregated chunk insights (Revision {current_count + 1})...")

    # 5. 执行 API 调用
    try:
        model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4o")
        response = client.chat.completions.create(
            model=model_name, 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            # 融合节点需要将碎片化信息组织为流畅文章，因此适度提高 temperature 以获取更好的文笔和行文组织能力
            temperature=0.5, 
        )
        draft = response.choices[0].message.content
        print("  -> [Fusion Drafter Node] Draft synthesized successfully.")
        
        return {
            "draft_summary": draft,
            "revision_count": current_count + 1
        }
    except Exception as e:
        print(f"  -> [Fusion Drafter Node] Error during synthesis: {str(e)}")
        # 将异常上抛，由后续路由或最终结果展现
        return {
            "draft_summary": f"[系统自动提示]：综合图文大纲失败，LLM 调用发生异常：{str(e)}",
            "revision_count": current_count + 1
        }