import os
import httpx
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("LLM_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "mistralai/mistral-7b-instruct"

def summarize_text(text: str) -> str:
    try:
        print(f"🧠 Summarizing using model: {OPENROUTER_MODEL}")
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://venkyautopilotai.com",  # optional
            "X-Title": "AutopilotAI-TelegramBot"
        }
        payload = {
            "model": OPENROUTER_MODEL,
            "messages": [
                {"role": "system", "content": "Summarize the email in 2-3 sentences."},
                {"role": "user", "content": text}
            ]
        }
        response = httpx.post(OPENROUTER_BASE_URL, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        summary = response.json()["choices"][0]["message"]["content"]
        return summary.strip()
    except Exception as e:
        return f"[Summary Error] {str(e)}"

def polish_message(raw_message: str) -> str:
    try:
        print(f"✨ Polishing message via OpenRouter...")
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://venkyautopilotai.com",
            "X-Title": "AutopilotAI-TelegramBot"
        }
        payload = {
            "model": OPENROUTER_MODEL,
            "messages": [
                {"role": "system", "content": "Polish the given casual message into a professional email tone."},
                {"role": "user", "content": raw_message}
            ]
        }
        response = httpx.post(OPENROUTER_BASE_URL, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        polished = response.json()["choices"][0]["message"]["content"]
        return polished.strip()
    except Exception as e:
        return f"[Error polishing message] {str(e)}"

def parse_reminder_instruction(instruction: str) -> str:
    """
    Uses OpenRouter to convert a natural language reminder into JSON with time and message.
    Example prompt: "Remind me to pay bills tomorrow at 6pm"
    """
    try:
        print(f"⏰ Parsing reminder: {instruction}")
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://venkyautopilotai.com",
            "X-Title": "AutopilotAI-ReminderParser"
        }
        system_prompt = (
            "You are a helpful assistant that extracts structured reminder information.\n"
            "Given an instruction, return a JSON with two fields: 'time' (ISO 8601 format preferred) and 'message'."
        )
        payload = {
            "model": OPENROUTER_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": instruction}
            ]
        }
        response = httpx.post(OPENROUTER_BASE_URL, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        result = response.json()["choices"][0]["message"]["content"]
        return result.strip()
    except Exception as e:
        return f"[Error parsing reminder] {str(e)}"
