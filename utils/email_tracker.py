import json
import os

TRACKER_FILE = "last_email.json"

def get_last_uid():
    if os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE, "r") as f:
            return json.load(f).get("last_uid", None)
    return None

def update_last_uid(uid):
    with open(TRACKER_FILE, "w") as f:
        json.dump({"last_uid": uid}, f)