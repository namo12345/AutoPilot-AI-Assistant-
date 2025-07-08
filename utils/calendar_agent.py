# utils/calendar_agent.py

import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

load_dotenv()

def get_calendar_service():
    creds = Credentials.from_authorized_user_info({
        "refresh_token": os.getenv("CALENDAR_REFRESH_TOKEN"),
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": os.getenv("CALENDAR_CLIENT_ID"),
        "client_secret": os.getenv("CALENDAR_CLIENT_SECRET")
    }, scopes=["https://www.googleapis.com/auth/calendar.events"])
    creds.refresh(Request())
    return build("calendar", "v3", credentials=creds)

def create_event(summary, description, start_time, duration_minutes=60):
    try:
        service = get_calendar_service()
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': (start_time + timedelta(minutes=duration_minutes)).isoformat(),
                'timeZone': 'Asia/Kolkata',
            },
        }

        created_event = service.events().insert(calendarId='primary', body=event).execute()
        return f"✅ Reminder set: {created_event.get('htmlLink')}"
    except Exception as e:
        return f"❌ Failed to set reminder: {str(e)}"
