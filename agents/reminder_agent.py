# agents/reminder_agent.py

import os
from datetime import timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv
import dateparser

load_dotenv()

# Build Google Calendar service
def get_calendar_service():
    creds = Credentials(
        None,
        refresh_token=os.getenv("CALENDAR_REFRESH_TOKEN"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("CALENDAR_CLIENT_ID"),
        client_secret=os.getenv("CALENDAR_CLIENT_SECRET"),
    )
    return build("calendar", "v3", credentials=creds)

# Create Google Calendar event
def create_calendar_event(summary, start_time, end_time=None):
    try:
        service = get_calendar_service()

        if end_time is None:
            end_time = start_time + timedelta(hours=1)

        event = {
            "summary": summary,
            "start": {"dateTime": start_time.isoformat(), "timeZone": "Asia/Kolkata"},
            "end": {"dateTime": end_time.isoformat(), "timeZone": "Asia/Kolkata"},
        }

        result = service.events().insert(calendarId="primary", body=event).execute()
        return f"✅ Reminder set: {result.get('summary')} at {start_time.strftime('%I:%M %p on %d %b %Y')}"
    except Exception as e:
        return f"❌ Calendar Error: {str(e)}"

# Natural-language based reminder creation
def create_reminder(natural_time, task):
    try:
        parsed_time = dateparser.parse(natural_time, settings={"TIMEZONE": "Asia/Kolkata", "RETURN_AS_TIMEZONE_AWARE": False})

        if not parsed_time:
            return "⚠️ Could not understand the time. Try saying something like 'today at 6pm'."

        return create_calendar_event(task, parsed_time)

    except Exception as e:
        return f"❌ Reminder Error: {str(e)}"
