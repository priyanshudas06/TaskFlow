from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import asyncio
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

if not MONGO_DB_NAME:
	raise ValueError("Environment variable 'taskManager' for database name is not set.")

client = AsyncIOMotorClient(MONGO_URL)
db = client[MONGO_DB_NAME]
task_collection = db["tasks"]
user_collection = db["users"]
refresh_token_collection = db["refresh_tokens"]
