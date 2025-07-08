import os
import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from telegram import Update
from telegram.ext import ContextTypes
from utils.llm_util import summarize_text
from agents.attachment_summarizer import save_attachment

# Load from .env
GMAIL_USER = os.getenv("GMAIL_USER")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REFRESH_TOKEN = os.getenv("GOOGLE_REFRESH_TOKEN")

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    creds = Credentials(
        None,
        refresh_token=GOOGLE_REFRESH_TOKEN,
        token_uri='https://oauth2.googleapis.com/token',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        scopes=SCOPES
    )
    return build('gmail', 'v1', credentials=creds)

async def summarize_mail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("📨 Fetching your latest emails...")

        service = get_gmail_service()
        result = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=5).execute()
        messages = result.get('messages', [])

        if not messages:
            await update.message.reply_text("📭 No new emails found.")
            return

        summaries = []

        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
            headers = msg_data.get("payload", {}).get("headers", [])
            subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")

            parts = msg_data.get("payload", {}).get("parts", [])
            body = ""

            # Extract plain text part of the email
            for part in parts:
                if part["mimeType"] == "text/plain":
                    body_data = part["body"].get("data", "")
                    body = base64.urlsafe_b64decode(body_data).decode("utf-8")
                    break

            if body.strip():
                summary = summarize_text(body[:2000])
                summaries.append(f"✉️ *{subject}*\n{summary}")

            # Check for and summarize attachments
            attachment_summary = save_attachment(service, msg['id'], parts)
            for filename, summary in attachment_summary:
                summaries.append(f"📎 *{filename}* (Attachment)\n{summary}")

        for s in summaries:
            await update.message.reply_text(s, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"❌ Failed to summarize emails: {str(e)}")
