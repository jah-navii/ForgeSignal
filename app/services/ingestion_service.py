import tweepy
import praw
import requests
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

class RedditIngestor:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=Config.REDDIT_CLIENT_ID,
            client_secret=Config.REDDIT_SECRET,
            user_agent=Config.REDDIT_USER_AGENT,
        )

    def fetch_subreddit_posts(self, subreddit_name: str, limit: int = 20):
        logger.info(f"Fetching posts from r/{subreddit_name}")
        subreddit = self.reddit.subreddit(subreddit_name)
        posts = [
            {
                "id": post.id,
                "title": post.title,
                "text": post.selftext,
                "created_utc": post.created_utc,
            }
            for post in subreddit.hot(limit=limit)
        ]
        logger.info(f"Fetched {len(posts)} posts.")
        return posts

    @staticmethod
    def serialize_docs(docs):
        """
        Convert MongoDB docs (with ObjectId) into JSON-serializable dicts.
        """
        from bson import ObjectId

        serialized = []
        for d in docs:
            d = dict(d)
            if "_id" in d and isinstance(d["_id"], ObjectId):
                d["_id"] = str(d["_id"])
            serialized.append(d)
        return serialized
    

class NewsFeedIngestor:
    def __init__(self):
        self.api_key = Config.NEWSAPI_KEY
        self.base_url = "https://newsapi.org/v2/everything"

    def fetch_news(self, query: str, page_size: int = 20, language: str = "en"):
        """
        Fetch recent financial news articles based on query.
        """
        logger.info(f"Fetching news articles for query: {query}")
        params = {
            "q": query,
            "language": language,
            "pageSize": page_size,
            "sortBy": "publishedAt",
            "apiKey": self.api_key,
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            articles = [
                {
                    "id": idx,
                    "source": a.get("source", {}).get("name"),
                    "title": a.get("title"),
                    "description": a.get("description"),
                    "url": a.get("url"),
                    "published_at": a.get("publishedAt"),
                    "content": a.get("content"),
                }
                for idx, a in enumerate(data.get("articles", []))
            ]

            logger.info(f"Fetched {len(articles)} articles.")
            return articles

        except Exception as e:
            logger.error(f"Error fetching news: {str(e)}")
            return []

