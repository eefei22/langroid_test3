from app.models.journal import JournalEntry
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to MongoDB Atlas
MONGO_URI = os.getenv("MONGODB_URI")
client = AsyncIOMotorClient(MONGO_URI)

# ✅ Use correct DB and collection names
db = client["Wellness_Engagement"]
journal_collection = db["journals"]

async def save_entry(entry: JournalEntry):
    await journal_collection.insert_one(entry.dict())
