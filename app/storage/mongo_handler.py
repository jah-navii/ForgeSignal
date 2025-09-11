from pymongo import MongoClient
from app.utils.config import Config
from app.utils.logger import logger

class MongoHandler:
    def __init__(self):
        self.client = MongoClient(Config.DB_URI)
        self.db = self.client["sentiment_engine"]

    def insert_data(self, collection_name, data):
        collection = self.db[collection_name]
        if isinstance(data, list):
            result = collection.insert_many(data)
            logger.info(f"Inserted {len(result.inserted_ids)} documents into '{collection_name}' collection.")
        else:
            result = collection.insert_one(data)
            logger.info(f"Inserted document with id {result.inserted_id} into '{collection_name}' collection.")

    def fetch_data(self, collection_name, limit=20):
        collection = self.db[collection_name]
        documents = list(collection.find().sort("created_at", -1).limit(limit))
        # Convert ObjectId to string for FastAPI JSON compatibility
        for doc in documents:
            doc["_id"] = str(doc["_id"])
        logger.info(f"Fetched {len(documents)} documents from '{collection_name}' collection.")
        return documents
