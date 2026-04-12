import os
import json
import urllib.request
import urllib.parse

def execute_tavily_search(query: str) -> str:
    """
    [多模态主动求知工具]：执行 Tavily 文本搜索，获取最新的互联网百科、热词释义。
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        # [优雅降级拦截]：如果没配 key，让模型使用内部知识盲猜，不让整个 LangGraph 崩溃
        return "Tool Execution Failed: TAVILY_API_KEY is not configured. Please proceed with your internal pre-trained knowledge."
        
    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}
    data = json.dumps({
        "api_key": api_key,
        "query": query,
        "search_depth": "basic",
        "include_answer": False,
        "max_results": 3
    }).encode("utf-8")
    
    try:
        # 使用 Python 原生 urllib 以遵守架构“少引入非必要第三方库”的教条
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))
            snippets = [r.get("content", "") for r in result.get("results", [])]
            if snippets:
                return "Web Search Results:\n" + "\n".join(snippets)
            return "Web Search Results: No relevant information found on the internet."
    except Exception as e:
        return f"Tool Execution Failed: Network error -> {str(e)}. Please proceed with your internal knowledge."