import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv("backend/.env")

uri = os.getenv("MONGO_URI")
print(f"Connecting to: {uri}")

client = MongoClient(uri)

try:
    client.admin.command("ping")
    print("MongoDB connected successfully!")
except Exception as e:
    print("MongoDB connection failed:", e)