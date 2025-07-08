# utils/deep_research_agent.py

import os
import requests
from dotenv import load_dotenv
from utils.llm_util import summarize_text

load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def search_web(query, max_results=5):
    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "advanced",
        "max_results": max_results,
        "include_answer": False,
        "include_raw_content": True
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        raise Exception(f"Tavily API error: {response.status_code} - {response.text}")

def research_topic(topic: str) -> str:
    try:
        results = search_web(topic)
        combined_content = "\n\n".join([res.get("content", "") for res in results])
        if not combined_content.strip():
            return "⚠️ No useful content found. Try a different topic."
        
        summary = summarize_text(combined_content)
        return f"📚 *Deep Research Summary for:* _{topic}_\n\n{summary}"
    except Exception as e:
        return f"❌ Research agent error: {str(e)}"
def generate_research_report(query):
    try:
        results = search_web(query)
        combined_content = "\n\n".join([res.get("content", "") for res in results])
        if not combined_content.strip():
            return "No useful web content found. Try a different topic."
        summary = summarize_text(combined_content)
        return summary
    except Exception as e:
        return f"❌ Research agent error: {str(e)}"
