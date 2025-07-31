from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("mongodb+srv://priyanshudas:<Leeza%231976>@cluster0.xauzpqm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

if not MONGO_DB_NAME:
	raise ValueError("Environment variable 'taskManager' for database name is not set.")

client = AsyncIOMotorClient(MONGO_URL)
db = client[MONGO_DB_NAME]
task_collection = db["tasks"]
