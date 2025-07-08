import base64
import os
import mimetypes
from googleapiclient.discovery import build
from utils.llm_util import summarize_text

import fitz  # PyMuPDF for PDFs
import pandas as pd
import docx

DOWNLOAD_PATH = "attachments"

def save_attachment(service, msg_id, parts):
    if not os.path.exists(DOWNLOAD_PATH):
        os.makedirs(DOWNLOAD_PATH)

    summaries = []

    for part in parts:
        filename = part.get("filename")
        if filename:
            attachment_id = part["body"].get("attachmentId")
            if attachment_id:
                attachment = service.users().messages().attachments().get(
                    userId="me", messageId=msg_id, id=attachment_id
                ).execute()

                data = base64.urlsafe_b64decode(attachment["data"].encode("UTF-8"))
                file_path = os.path.join(DOWNLOAD_PATH, filename)

                with open(file_path, "wb") as f:
                    f.write(data)

                # Summarize the file
                summary = summarize_attachment(file_path)
                if summary:
                    summaries.append((filename, summary))

    return summaries

def summarize_attachment(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    text = ""

    try:
        if file_path.endswith(".pdf"):
            doc = fitz.open(file_path)
            for page in doc:
                text += page.get_text()
            doc.close()

        elif file_path.endswith(".docx"):
            doc = docx.Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])

        elif file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
            text = df.to_string(index=False)

        if text.strip():
            return summarize_text(text[:2000])  # Limit input
    except Exception as e:
        return f"[Attachment Summary Error] {str(e)}"

    return None
