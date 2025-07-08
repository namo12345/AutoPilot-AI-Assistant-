import os
import json
import httpx
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("LLM_API_KEY")

def parse_intent_with_llm(user_input: str) -> dict:
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        prompt = f"""
        Classify the user's command and extract intent + entities in JSON.
        Instructions:
        - Recognize email addresses with or without spaces, and clean them.
        - Identify reminder commands with task + time.
        - Recognize research-related prompts.

        Examples:
        - "summarize my email" → {{ "intent": "summarize_mails" }}
        - "remind me tomorrow 8pm to call Sana" → {{ "intent": "set_reminder", "task": "call Sana", "time": "tomorrow 8pm" }}
        - "send email to venkyreddy6155@gmail.com saying I hate you" → {{ "intent": "send_email", "email": "venkyreddy6155@gmail.com", "message": "I hate you" }}
        - "do research about RAGs in AI" → {{ "intent": "do_research", "topic": "RAGs in AI" }}
        - "research topic RAGs" → {{ "intent": "research", "topic": "RAGs" }}

        Now handle: "{user_input}"
        """

        body = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [{"role": "user", "content": prompt}]
        }

        response = httpx.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)

        if response.status_code != 200:
            print(f"[LLM API Error] {response.status_code} - {response.text}")
            return {}

        data = response.json()
        print("[LLM Raw Response]", json.dumps(data, indent=2))

        if "choices" not in data or not data["choices"]:
            print("[LLM Response Error] Missing 'choices' in LLM response")
            return {}

        content = data["choices"][0]["message"]["content"]
        return json.loads(content)

    except Exception as e:
        print(f"[LLM Parse Error] {str(e)}")
        return {}
