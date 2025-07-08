import os
import json
import pickle
import webbrowser
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Scope to access Google Calendar
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

# Path to your new client_secret file for calendar
CLIENT_SECRET_FILE = "client_secret_calendar.json"
TOKEN_PICKLE = "token_calendar.pickle"

def generate_calendar_token():
    creds = None

    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(TOKEN_PICKLE, 'wb') as token:
            pickle.dump(creds, token)

    print("\n✅ COPY this new refresh token and add it to your .env:")
    print(f"CALENDAR_REFRESH_TOKEN={creds.refresh_token}")

if __name__ == '__main__':
    generate_calendar_token()
