from fastapi import APIRouter, Query
from app.services.ingestion_service import TwitterIngestor, RedditIngestor, NewsFeedIngestor
from app.storage.mongo_handler import MongoHandler
from app.utils.logger import logger

router = APIRouter(prefix="/ingestion", tags=["Data Ingestion"])

mongo = MongoHandler()
twitter = TwitterIngestor()
reddit = RedditIngestor()
news = NewsFeedIngestor()

def serialize_docs(docs):
    """Convert ObjectId to string for JSON serialization."""
    for doc in docs:
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
    return docs


@router.get("/twitter/live")
def fetch_live_tweets(query: str = Query(..., description="Search query"),
                      max_results: int = Query(20, ge=10, le=100)):

    logger.info(f"Fetching live tweets for query={query}")
    tweets = twitter.fetch_recent_tweets(query=query, max_results=max_results)
    if tweets:
        mongo.insert_data("twitter_data", tweets)
    return {"source": "twitter", "fetched": len(tweets), "data": serialize_docs(tweets)}


@router.get("/twitter/cache")
def fetch_cached_tweets(limit: int = Query(20, ge=1, le=100)):
    """
    Fetch tweets from MongoDB cache instead of hitting Twitter API.
    ✅ Safe for repeated testing.
    """
    logger.info(f"Fetching cached tweets, limit={limit}")
    tweets = mongo.fetch_data("twitter_data", limit=limit)
    return {"source": "twitter_cache", "fetched": len(tweets), "data": tweets}


@router.get("/reddit/live")
def fetch_live_reddit_posts(
    subreddit: str = Query(..., description="Subreddit name"),
    limit: int = Query(20, ge=1, le=100),
):
    """
    Fetch live posts from a subreddit and save them to MongoDB.
    """
    logger.info(f"Fetching live Reddit posts for r/{subreddit}")
    posts = reddit.fetch_subreddit_posts(subreddit_name=subreddit, limit=limit)
    if posts:
        mongo.insert_data("reddit_data", posts)
    return {
        "source": f"reddit:{subreddit}",
        "fetched": len(posts),
        "data": reddit.serialize_docs(posts),
    }


@router.get("/reddit/cache")
def fetch_cached_reddit_posts(
    limit: int = Query(20, ge=1, le=100),
):
    """
    Fetch cached Reddit posts from MongoDB (no API call).
    """
    logger.info(f"Fetching cached Reddit posts, limit={limit}")
    posts = mongo.fetch_data("reddit_data", limit=limit)
    return {
        "source": "reddit_cache",
        "fetched": len(posts),
        "data": RedditIngestor.serialize_docs(posts),
    }

@router.get("/news/live")
def fetch_live_news(
    query: str = Query(..., description="Search topic or financial keyword"),
    page_size: int = Query(20, ge=5, le=100),
):
    """
    Fetch live financial news articles using the configured news API.
    Stores the results in MongoDB for caching.
    """
    logger.info(f"Fetching live news for query='{query}'")
    articles = news.fetch_news(query=query, page_size=page_size)
    if articles:
        mongo.insert_data("news_data", articles)
    return {
        "source": "news_live",
        "fetched": len(articles),
        "data": serialize_docs(articles),
    }

@router.get("/news/cache")
def fetch_cached_news(
    limit: int = Query(20, ge=1, le=100),
):
    """
    Fetch cached news articles from MongoDB instead of hitting the live API.
    Useful for testing and analytics.
    """
    logger.info(f"Fetching cached news, limit={limit}")
    articles = mongo.fetch_data("news_data", limit=limit)
    return {
        "source": "news_cache",
        "fetched": len(articles),
        "data": serialize_docs(articles),
    }

