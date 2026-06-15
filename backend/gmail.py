import base64
import os
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


def get_gmail_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "backend/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def get_emails(service, max_results=5):
    results = (
        service.users().messages().list(userId="me", maxResults=max_results).execute()
    )
    messages = results.get("messages", [])
    emails = []
    for msg in messages:
        txt = service.users().messages().get(userId="me", id=msg["id"]).execute()
        headers = txt["payload"]["headers"]
        email = {}
        for header in headers:
            if header["name"] == "Subject":
                email["subject"] = header["value"]
            if header["name"] == "From":
                email["from"] = header["value"]
        emails.append(email)
    return emails


def compose_email(services, to, subject, body, cc=None):
    msg = MIMEText(body, "plain")
    msg["to"] = to
    msg["subject"] = subject
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    print(f"To:{to}\n Subject:{subject}\n Body:{body} ")
    services.users().messages().send(userId="me", body={"raw": raw}).execute()
