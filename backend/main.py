from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
from pydantic import BaseModel
from fastapi import UploadFile, File
import PyPDF2
from mongo_db import save_message, load_history

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
conversation_history = load_history()
class ChatInput(BaseModel):
    content:str
@app.post("/chat")
async def chat(message:ChatInput):
    user_message = message.content 
    conversation_history.append({"role": "user", "content": user_message})
    save_message("user", user_message)
    full_prompt = ""
    for msg in conversation_history:
        full_prompt += msg["role"] + ": " + msg["content"] + "\n"
    async with httpx.AsyncClient(timeout=60) as client: 
        response =await client.post(
        "http://localhost:11434/api/generate",
        json={
            "model":"llama3.2",
            "system": "You are GURU, Raghava's personal assistant. Raghava is a CS engineering student from Thirthahalli getting ready for the software world. He loves philosophy, books, movies, and solving NeetCode problems. He has crazy goals — building a university like Takshashila, creating PersonaOS, and restoring Bharat's knowledge systems. Talk straight, be honest, use humor, weak English is fine, never be fake. "
            "Respond naturally to what he says. Don't repeat yourself. Don't ask the same questions. If he's joking, joke back. If he's working, help him work. Read the conversation history and continue from where you left off — not from the beginning. Be honest, use humor, challenge him when wrong.",
            "prompt":full_prompt,
            "stream":False

        }
    )
    result=response.json()
    conversation_history.append({"role": "assistant", "content": result["response"]})
    save_message("assistant", result["response"])
    return {"response":result["response"]}

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8000)


  

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    # Read PDF
    pdf_reader = PyPDF2.PdfReader(file.file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    # Send to Ollama (same as chat)
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": f"Read this and answer questions about it: {text[:2000]}",  # limit length
                "stream": False
            }
        )
    result = response.json()
    return {"response": result["response"]}

