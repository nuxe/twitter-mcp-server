# Twitter MCP Server

A minimal Python MCP server for X (Twitter) with 3 core tools. Built for the free tier (100 reads, 500 posts/month).

## Features

- **get_home_timeline** - Read your timeline
- **create_tweet** - Post new tweets  
- **reply_to_tweet** - Reply to tweets

## Setup

### 1. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Twitter API Setup

1. Create a Twitter Developer account at https://developer.twitter.com/
2. Create a new app and get your API credentials
3. Create a `.env` file using the template provided in `twitter_credentials_template.txt`:

```bash
cp twitter_credentials_template.txt .env
# Edit .env with your actual credentials
```

### 3. Configure Claude Desktop

Add this to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "twitter": {
      "command": "python",
      "args": ["/absolute/path/to/twitter-mcp-server/server.py"],
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

### 4. Test the Server

```bash
python server.py
```

### 5. Restart Claude Desktop

After configuration, restart Claude Desktop to load the MCP server.

## Usage

Once configured, you can use these tools in Claude:

- **Read Timeline**: "Show me my recent tweets from Twitter"
- **Post Tweet**: "Tweet 'Hello from Claude!' to Twitter"
- **Reply to Tweet**: "Reply to tweet ID 1234567890 with 'Great point!'"

## Rate Limits

This server is designed for Twitter's free tier:
- 100 reads per month
- 500 posts per month

## Tech Stack

- Python 3.10+
- MCP SDK
- Tweepy (Twitter API v2)
- Environment variables for credentials 