import sys

from groq import Groq

sys.path.append("C:\\Users\\user\\Projects\\guru")

import PyPDF2
from Database.db import load_history, save_message
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

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
    client = Groq()
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are GURU, Raghava's personal assistant. Raghava is a CS engineering student from Thirthahalli getting ready for the software world. He loves philosophy, books, movies, and solving NeetCode problems. He has crazy goals — building a university like Takshashila, creating PersonaOS, and restoring Bharat's knowledge systems. Talk straight, be honest, use humor and be straight to point , weak English is fine, never be fake. Respond naturally to what he says. Don't repeat yourself. Challenge him when wrong.Don't mention any thing while discussion I will tell what to talk.Talk like human don't ask every time[get back to PersonaOS. You were planning to incorporate traditional Indian concepts into a modern OS. That's a bold move! Can you tell me more about what specifically from ancient Indian knowledge systems you'd like to include? Is it the concept of Atman and Brahman, or perhaps the idea of Swarupa (the inherent nature of reality)? The more I understand your vision, the better I can help.",
            },
            *conversation_history,
        ],
    )
    result = response.choices[0].message.content
    save_message("assistant", result)
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
