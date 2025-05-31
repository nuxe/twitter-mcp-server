import asyncio
import os
import tweepy
from mcp.server.fastmcp import FastMCP
from mcp.server.stdio import stdio_server

# Initialize MCP server
app = FastMCP("twitter-mcp-server")

# Initialize Twitter client
client = tweepy.Client(
    consumer_key=os.environ.get("TWITTER_API_KEY"),
    consumer_secret=os.environ.get("TWITTER_API_SECRET"),
    access_token=os.environ.get("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.environ.get("TWITTER_ACCESS_TOKEN_SECRET"),
    bearer_token=os.environ.get("TWITTER_BEARER_TOKEN")
)

@app.tool()
async def get_home_timeline(limit: int = 20) -> str:
    """Get recent tweets from your home timeline"""
    try:
        response = client.get_home_timeline(max_results=min(limit, 100))
        tweets = []
        for tweet in response.data or []:
            tweets.append(f"@{tweet.author_id}: {tweet.text}")
        return "\n\n".join(tweets) if tweets else "No tweets found"
    except Exception as e:
        return f"Error: {str(e)}"

@app.tool()
async def create_tweet(text: str) -> str:
    """Create a new tweet (max 280 characters)"""
    if len(text) > 280:
        return "Error: Tweet exceeds 280 characters"
    try:
        response = client.create_tweet(text=text)
        tweet_id = response.data['id']
        return f"Tweet posted successfully: https://twitter.com/user/status/{tweet_id}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.tool()
async def reply_to_tweet(tweet_id: str, text: str) -> str:
    """Reply to a tweet"""
    if len(text) > 280:
        return "Error: Reply exceeds 280 characters"
    try:
        response = client.create_tweet(text=text, in_reply_to_tweet_id=tweet_id)
        reply_id = response.data['id']
        return f"Reply posted successfully: https://twitter.com/user/status/{reply_id}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    asyncio.run(stdio_server(app)) 