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


def read_email(services, max_results=5):
    results = (
        services.users().messages().list(userId="me", maxResults=max_results).execute()
    )
    messages = results.get("messages", [])
    for msg in messages:
        txt = services.users().messages().get(userId="me", id=msg["id"]).execute()
        payload = txt["payload"]
        headers = payload["headers"]
        for header in headers:
            if header["name"] == "Subject":
                print("Subject:", header["value"])
            if header["name"] == "From":
                print("From", header["value"])
        print("---------")


def compose_email(services, to, subject, body, cc=None):
    msg = MIMEText(body, "plain")
    msg["to"] = to
    msg["subject"] = subject
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    print(f"To:{to}\n Subject:{subject}\n Body:{body} ")
    confirm = input("Send(y/n):")
    if confirm != "y":
        return
    services.users().messages().send(userId="me", body={"raw": raw}).execute()


if __name__ == "__main__":
    service = get_gmail_service()
    read_email(service)
    compose_email(service, "ayyajiraghavas@gmail.com", "Test", "Hello from GURU")
