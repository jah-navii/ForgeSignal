import tweepy
from app.utils.config import Config
from app.utils.logger import logger

class TwitterIngestor:
    def __init__(self):
        self.client = tweepy.Client(bearer_token=Config.TWITTER_BEARER_TOKEN)

    def fetch_recent_tweets(self, query, max_results=50):
        logger.info(f"Fetching tweets for query: {query}")
        response = self.client.search_recent_tweets(query=query, max_results=max_results, tweet_fields=["created_at", "author_id", "lang"])
        tweets = [{"id": t.id, "text": t.text, "created_at": t.created_at, "author_id": t.author_id} for t in response.data or []]
        logger.info(f"Fetched {len(tweets)} tweets.")
        return tweets
