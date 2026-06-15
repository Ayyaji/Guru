import os
import sys

from groq import Groq

sys.path.insert(0, os.path.abspath("C:\\Users\\user\\Projects\\guru"))

import PyPDF2
from backend.extract import parse_and_execute
from backend.gmail import compose_email, get_emails, get_gmail_service
from Database.db import load_history, save_message
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()
client = Groq()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatInput(BaseModel):
    content: str


@app.post("/chat")
async def chat(message: ChatInput):
    conversation_history = load_history(limit=20)
    user_message = message.content
    save_message("user", user_message)
    conversation_history.append({"role": "user", "content": user_message})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are GURU, Raghava's personal assistant...",
            },
            *conversation_history,
        ],
    )
    result = response.choices[0].message.content
    save_message("assistant", result)
    parse_and_execute(result)
    return {"response": result}


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    pdf_reader = PyPDF2.PdfReader(file.file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    client = Groq()
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"Read this and answer questions about it: {text[:2000]}",
            }
        ],
    )
    return {"response": response.choices[0].message.content}


class EmailInput(BaseModel):
    to: str
    subject: str
    body: str


@app.get("/read-email")
async def fetch_emails():
    service = get_gmail_service()
    return {"emails": get_emails(service)}


@app.post("/send-email")
async def send_email(data: EmailInput):
    service = get_gmail_service()
    compose_email(service, data.to, data.subject, data.body)
    return {"status": "sent"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
