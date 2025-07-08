import os
import base64
import httpx
from email.mime.text import MIMEText
from dotenv import load_dotenv

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_MODEL = "mistralai/mistral-7b-instruct"

def get_gmail_service():
    creds = Credentials.from_authorized_user_info({
        "refresh_token": os.getenv("GOOGLE_REFRESH_TOKEN"),
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET")
    }, scopes=SCOPES)
    creds.refresh(Request())
    return build("gmail", "v1", credentials=creds)

def create_message(to, subject, message_text):
    message = MIMEText(message_text)
    message["to"] = to
    message["subject"] = subject
    return {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")}

def polish_message(raw_input: str) -> str:
    prompt = f"""
You are an AI email assistant. Convert the user's message into a complete email.
Preserve the original tone and intent. Do NOT use overly formal tone unless required.

Message: "{raw_input}"

Write the full email:
"""
    body = {
        "model": LLM_MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }

    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = httpx.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[❌ Error polishing message] {str(e)}")
        return raw_input  # fallback

def send_email_with_gpt(receiver_email, short_msg):
    try:
        service = get_gmail_service()

        polished_msg = polish_message(short_msg)
        subject = "📧 Message from AI Assistant"

        message = create_message(receiver_email, subject, polished_msg)
        service.users().messages().send(userId="me", body=message).execute()

        return f"✅ Email sent to {receiver_email} with polished message: \n\n{polished_msg}"

    except Exception as e:
        return f"❌ Failed to send email: {str(e)}"
