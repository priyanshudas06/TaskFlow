from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("mongodb+srv://priyanshudas:<Leeza%231976>@cluster0.xauzpqm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
MONGGO_DB_NAME = os.getenv("taskManager")

client = AsyncIOMotorClient(MONGO_URL)
db = client[MONGGO_DB_NAME] # type: ignore
