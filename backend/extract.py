import json
import os
import sys

from groq import Groq

sys.path.insert(0, os.path.abspath("C:\\Users\\user\\Projects\\guru"))
from backend.gmail import compose_email, get_gmail_service
from Database.db import load_history, save_message
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
app = FastAPI()


def parse_and_execute(guru_response):
    client = Groq()
    system_prompt = (
        "You are an intent extractor. Given a text, "
        "return ONLY a JSON object with keys: action, to, subject, body. "
        "For sending emails, action must be exactly 'send_email'. "
        "If no action is detected, return {'action': 'none'}. "
        "No explanation, no markdown, just raw JSON."
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": guru_response},
        ],
    )
    raw = response.choices[0].message.content
    print("Extract raw output:", raw)
    result = json.loads(raw)
    print("Parsed result:", result)
    result = json.loads(response.choices[0].message.content)
    if result["action"] == "send_email":
        service = get_gmail_service()
        compose_email(service, result["to"], result["subject"], result["body"])
