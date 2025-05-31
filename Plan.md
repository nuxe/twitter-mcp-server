# Twitter MCP Server - Python Tech Spec

## Overview
A minimal Python MCP server for X (Twitter) with 3 core tools. Built for the free tier (100 reads, 500 posts/month).

## Tech Stack
- **Python 3.10+**
- **MCP SDK** (`mcp`)
- **Tweepy** (Twitter API v2)
- **Environment variables** for credentials

## Core Tools (3 Only)
1. `get_home_timeline` - Read your timeline
2. `create_tweet` - Post new tweets  
3. `reply_to_tweet` - Reply to tweets

## Project Structure
```
twitter-mcp-server/
├── server.py              # Main MCP server (all code here)
├── .env                   # Credentials
├── requirements.txt       # Dependencies
└── README.md
```

## Implementation (2 hours)

### Step 1: Setup (15 mins)
```bash
mkdir twitter-mcp-server && cd twitter-mcp-server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install mcp tweepy python-dotenv
```

### Step 2: Core Implementation (90 mins)

**requirements.txt:**
```
mcp
tweepy
python-dotenv
```

**server.py (complete implementation):**
```python
import asyncio
import os
import tweepy
from mcp.server.fastmcp import FastMCP
from mcp.server.stdio import stdio_server
from dotenv import load_dotenv

load_dotenv()

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
```

**.env:**
```bash
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
TWITTER_BEARER_TOKEN=your_bearer_token
```

### Step 3: Configuration (15 mins)

**Claude Desktop config** (`%APPDATA%/Claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "twitter": {
      "command": "python",
      "args": ["path/to/twitter-mcp-server/server.py"],
      "env": {
        "TWITTER_API_KEY": "your_api_key",
        "TWITTER_API_SECRET": "your_api_secret", 
        "TWITTER_ACCESS_TOKEN": "your_access_token",
        "TWITTER_ACCESS_TOKEN_SECRET": "your_access_token_secret",
        "TWITTER_BEARER_TOKEN": "your_bearer_token"
      }
    }
  }
}
```

## Essential Documentation for Cursor

**Feed these 5 URLs to Cursor:**

1. **MCP Python SDK:** https://github.com/modelcontextprotocol/python-sdk
2. **MCP Python Tutorial:** https://www.digitalocean.com/community/tutorials/mcp-server-python  
3. **Tweepy Documentation:** https://docs.tweepy.org/en/latest/
4. **Tweepy Examples:** https://docs.tweepy.org/en/stable/examples.html
5. **Create Tweet Example:** https://github.com/tweepy/tweepy/blob/master/examples/API_v2/create_tweet.py

**Cursor Prompt:**
> "Build a Python MCP server for X (Twitter) using the MCP SDK and Tweepy. Create exactly 3 tools: get_home_timeline, create_tweet, and reply_to_tweet. Use the FastMCP pattern, async/await, proper error handling, and environment variables for credentials. Keep it simple - all code in one server.py file."

## Testing
```bash
# Test locally
python server.py

# Test with Claude Desktop
# Restart Claude Desktop and use the tools in chat
```

## Success Criteria
- ✅ 3 tools working (timeline, tweet, reply)
- ✅ Proper rate limiting (free tier)
- ✅ Error handling for API failures
- ✅ Works with Claude Desktop
- ✅ Under 100 lines of code

## Time Estimate: 2 hours total
This is the simplest possible implementation that actually works.