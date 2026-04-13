from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/docs")
async def chat(message:dict):
    response =await client.post(
        "http://localhost:1143/api/generate",
        json={
            "model":"llama3.2",
            "prompts":user_message,
            "stream":False

        }
    )
    result=response.json()
    return {"response":result["response"]}

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8000)