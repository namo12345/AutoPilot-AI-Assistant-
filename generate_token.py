# generate_token.py
import os
import json
import logging
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify"
]

def main():
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

    if not client_id or not client_secret:
        print("❌ Client ID or Secret not found in .env")
        return

    flow = InstalledAppFlow.from_client_config(
        {
            "installed": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
            }
        },
        SCOPES,
    )

    creds = flow.run_local_server(port=0)
    print("\n✅ COPY this new refresh token and add it to your .env:\n")
    print("GOOGLE_REFRESH_TOKEN=" + creds.refresh_token)

    # Save for reuse (optional)
    with open("token.json", "w") as token_file:
        json.dump({
            "refresh_token": creds.refresh_token,
            "client_id": client_id,
            "client_secret": client_secret,
            "token_uri": "https://oauth2.googleapis.com/token"
        }, token_file)

if __name__ == "__main__":
    main()
