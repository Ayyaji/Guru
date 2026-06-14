from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import PyPDF2
from  db import save_message, load_history

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
    conversation_history.append({"role": "user", "content": user_message})
    save_message("user", user_message)
    full_prompt = ""
    for msg in conversation_history:
        full_prompt += msg["role"] + ": " + msg["content"] + "\n"
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "system": "You are GURU, Raghava's personal assistant. Raghava is a CS engineering student from Thirthahalli getting ready for the software world. He loves philosophy, books, movies, and solving NeetCode problems. He has crazy goals — building a university like Takshashila, creating PersonaOS, and restoring Bharat's knowledge systems. Talk straight, be honest, use humor and be straight to point , weak English is fine, never be fake. Respond naturally to what he says. Don't repeat yourself. Challenge him when wrong.Don't mention any thing while discussion I will tell what to talk.Talk like human don't ask every time[get back to PersonaOS. You were planning to incorporate traditional Indian concepts into a modern OS. That's a bold move! Can you tell me more about what specifically from ancient Indian knowledge systems you'd like to include? Is it the concept of Atman and Brahman, or perhaps the idea of Swarupa (the inherent nature of reality)? The more I understand your vision, the better I can help.]",
                "prompt": full_prompt,
                "stream": False
            }
        )
    result = response.json()
    save_message("assistant", result["response"])
    return {"response": result["response"]}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    pdf_reader = PyPDF2.PdfReader(file.file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": f"Read this and answer questions about it: {text[:2000]}",
                "stream": False
            }
        )
    result = response.json()
    return {"response": result["response"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)