import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def upload_video(channel_id, file, title, description, tags, category_id):
    AUTH_FILE = f"auth/tokens/{channel_id}.json"
    if not os.path.exists("auth/tokens"): os.makedirs("auth/tokens")
    creds = Credentials.from_authorized_user_file(AUTH_FILE, SCOPES) if os.path.exists(AUTH_FILE) else None
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token: creds.refresh(Request())
        else:
            creds =  InstalledAppFlow.from_client_secrets_file("auth/client_secret.json", SCOPES).run_local_server(port=0)
            with open(AUTH_FILE, "w") as token: token.write(creds.to_json())
            
    return build("youtube", "v3", credentials=creds).videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "categoryId": category_id,
                "description": description,
                "tags": tags,
                "title": title
            },
            "status": {
                "privacyStatus": "private"
            }
        },
        media_body=file
    ).execute()