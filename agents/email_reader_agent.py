# File: agents/email_reader_agent.py
import os
import base64
import tempfile
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from utils.llm_util import summarize_text
from utils.email_tracker import get_last_uid, update_last_uid
import fitz

load_dotenv()
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_gmail_service():
    creds = Credentials.from_authorized_user_info({
        "refresh_token": os.getenv("GOOGLE_REFRESH_TOKEN"),
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET")
    }, scopes=SCOPES)
    creds.refresh(Request())
    return build("gmail", "v1", credentials=creds)

def extract_text_from_pdf(data_bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(data_bytes)
        tmp_path = tmp_file.name
    doc = fitz.open(tmp_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    os.remove(tmp_path)
    return text.strip()

def extract_text_from_txt(data_bytes):
    return data_bytes.decode('utf-8', errors='ignore')

def handle_attachments(service, msg_id):
    try:
        attachment_texts = []
        message = service.users().messages().get(userId="me", id=msg_id).execute()
        parts = message.get("payload", {}).get("parts", [])
        for part in parts:
            filename = part.get("filename")
            body = part.get("body", {})
            if filename and "attachmentId" in body:
                att = service.users().messages().attachments().get(userId="me", messageId=msg_id, id=body["attachmentId"]).execute()
                data = base64.urlsafe_b64decode(att["data"].encode("UTF-8"))
                if filename.endswith(".pdf"):
                    summary = summarize_text(extract_text_from_pdf(data))
                    attachment_texts.append((filename, summary))
                elif filename.endswith(".txt"):
                    summary = summarize_text(extract_text_from_txt(data))
                    attachment_texts.append((filename, summary))
        return attachment_texts
    except Exception as e:
        return [("Error", f"Attachment processing error: {str(e)}")]

def fetch_latest_emails(n=1, label="INBOX"):
    service = get_gmail_service()
    results = service.users().messages().list(userId="me", labelIds=[label], maxResults=n).execute()
    messages = results.get("messages", [])

    last_msg_id = get_last_uid()
    new_emails = []
    latest_seen_id = last_msg_id

    for msg in reversed(messages):
        msg_id = msg["id"]
        if msg_id == last_msg_id:
            continue

        message = service.users().messages().get(userId="me", id=msg_id, format="metadata", metadataHeaders=["From", "Subject"]).execute()
        headers = message.get("payload", {}).get("headers", [])
        snippet = message.get("snippet", "")

        email_data = {
            "id": msg_id,
            "from": next((h["value"] for h in headers if h["name"] == "From"), ""),
            "subject": next((h["value"] for h in headers if h["name"] == "Subject"), ""),
            "snippet": snippet,
            "summary": summarize_text(snippet),
            "attachments": handle_attachments(service, msg_id)
        }

        new_emails.append(email_data)
        latest_seen_id = msg_id

    if latest_seen_id != last_msg_id:
        update_last_uid(latest_seen_id)

    return new_emails