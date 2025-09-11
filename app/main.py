# app/main.py
from fastapi import FastAPI
from app.routes import ingestion_router

app = FastAPI(title="Fear & Greed Sentiment Engine")

# # Initialize handlers
# mongo = MongoHandler()
# twitter = TwitterIngestor()

# @app.get("/ingest/twitter/live")
# def fetch_live_tweets(query: str = Query(..., description="Search query"),
#                       max_results: int = Query(20, ge=10, le=100)):

#     logger.info(f"Fetching live tweets for query={query}")
#     tweets = twitter.fetch_recent_tweets(query=query, max_results=max_results)
#     if tweets:
#         mongo.insert_data("twitter_data", tweets)
#     return {"source": "twitter", "fetched": len(tweets), "data": tweets}


# @app.get("/ingest/twitter/cache")
# def fetch_cached_tweets(limit: int = Query(20, ge=1, le=100)):
#     """
#     Fetch tweets from MongoDB cache instead of hitting Twitter API.
#     ✅ Safe for repeated testing.
#     """
#     logger.info(f"Fetching cached tweets, limit={limit}")
#     tweets = mongo.fetch_data("twitter_data", limit=limit)
    # return {"source": "twitter_cache", "fetched": len(tweets), "data": tweets}

app.include_router(ingestion_router.router)
