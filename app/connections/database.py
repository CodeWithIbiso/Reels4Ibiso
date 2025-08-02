import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URI"))
        self.db = self.client[os.getenv("MONGO_DB")]

    def get_collection(self, name: str):
        return self.db[name]

# Singleton instance of the database
database = Database()