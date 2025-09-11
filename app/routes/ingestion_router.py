from fastapi import APIRouter, Query
from app.services.ingestion_service import TwitterIngestor
from app.storage.mongo_handler import MongoHandler

router = APIRouter(prefix="/ingestion", tags=["Data Ingestion"])

mongo = MongoHandler()
twitter = TwitterIngestor()

def serialize_docs(docs):
    """Convert ObjectId to string for JSON serialization."""
    for doc in docs:
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
    return docs

@router.get("/ingest/twitter/live")
def fetch_live_tweets(query: str = Query(..., description="Search query"),
                      max_results: int = Query(20, ge=10, le=100)):

    # logger.info(f"Fetching live tweets for query={query}")
    tweets = twitter.fetch_recent_tweets(query=query, max_results=max_results)
    if tweets:
        mongo.insert_data("twitter_data", tweets)
    return {"source": "twitter", "fetched": len(tweets), "data": serialize_docs(tweets)}


@router.get("/ingest/twitter/cache")
def fetch_cached_tweets(limit: int = Query(20, ge=1, le=100)):
    """
    Fetch tweets from MongoDB cache instead of hitting Twitter API.
    ✅ Safe for repeated testing.
    """
    # logger.info(f"Fetching cached tweets, limit={limit}")
    tweets = mongo.fetch_data("twitter_data", limit=limit)
    return {"source": "twitter_cache", "fetched": len(tweets), "data": tweets}
