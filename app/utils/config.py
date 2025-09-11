import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    REDDIT_SECRET = os.getenv("REDDIT_SECRET")
    REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
    NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
    DB_URI = os.getenv("DB_URI", "mongodb://localhost:27017")
