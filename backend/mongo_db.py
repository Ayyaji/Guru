import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime

load_dotenv("backend/.env")

client=MongoClient(os.getenv("MONGO_URI"))
db=client["personaOS"]
conversations=db["conversations"]

def save_message(role:str,content:str):
    conversations.insert_one({
        "role":role,
        "content":content,
        "timestamp":datetime.now().isoformat()
    })

def load_history():
    message=conversations.find({},{"_id":0})
    return list(message)