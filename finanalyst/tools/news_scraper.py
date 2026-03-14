import requests
from bs4 import BeautifulSoup
import feedparser
from datetime import datetime
import pytz
from typing import List, Dict

# Standard time zone for consistency
IST = pytz.timezone('Asia/Kolkata')

# List of reliable financial RSS feeds
RSS_FEEDS = [
    "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",  # ET Markets
    "https://www.moneycontrol.com/rss/marketedge.xml",                      # MoneyControl
    "https://www.livemint.com/rss/markets",                                 # LiveMint Markets
]

def fetch_rss_news(limit_per_feed: int = 10) -> List[Dict]:
    """
    Fetches the latest financial news from predefined RSS feeds.
    
    Returns:
        A list of dictionaries containing news article data.
    """
    articles = []
    
    for feed_url in RSS_FEEDS:
        try:
            # Set a custom User-Agent to avoid getting blocked by anti-bot protections
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(feed_url, headers=headers, timeout=10)
            
            feed = feedparser.parse(response.content)
            print(f"Parsed {feed_url}: Found {len(feed.entries)} entries.")
            
            for entry in feed.entries[:limit_per_feed]:
                # Extract headline and summary
                title = entry.get('title', '').strip()
                summary = entry.get('summary', '').strip()
                
                # Basic cleanup using BeautifulSoup to remove HTML tags from summary
                if summary:
                    soup = BeautifulSoup(summary, 'html.parser')
                    summary = soup.get_text().strip()
                
                link = entry.get('link', '')
                
                # Parse timestamp if available, else use current time
                published_parsed = entry.get('published_parsed')
                if published_parsed:
                    dt = datetime(*published_parsed[:6])
                else:
                    dt = datetime.now()
                
                # Convert to IST format string
                dt_ist = dt.replace(tzinfo=pytz.utc).astimezone(IST)
                timestamp_str = dt_ist.strftime('%Y-%m-%d %H:%M:%S IST')
                
                articles.append({
                    "title": title,
                    "summary": summary,
                    "source": feed.feed.get('title', 'Unknown Source'),
                    "link": link,
                    "timestamp": timestamp_str,
                    "category": "Market News" # Default category
                })
        except Exception as e:
            print(f"Error fetching from {feed_url}: {e}")
            import traceback
            traceback.print_exc()
            
    # Sort by descending timestamp (newest first)
    articles.sort(key=lambda x: x['timestamp'], reverse=True)
    return articles


def deduplicate_news(articles: List[Dict]) -> List[Dict]:
    """
    Removes duplicate news articles based on title similarity/exact match.
    """
    seen_titles = set()
    unique_articles = []
    
    for article in articles:
        # Simple exact title match deduplication. Can be upgraded to fuzzy matching.
        title_lower = article['title'].lower()
        if title_lower not in seen_titles:
            seen_titles.add(title_lower)
            unique_articles.append(article)
            
    return unique_articles

def collect_latest_news() -> List[Dict]:
    """
    Main entry point for the news scraping tool.
    Fetches from RSS feeds and deduplicates.
    """
    raw_articles = fetch_rss_news()
    return deduplicate_news(raw_articles)

if __name__ == "__main__":
    # Test the scraper
    news = collect_latest_news()
    print(f"Fetched {len(news)} unique articles.")
    if news:
        print("\nLatest Article:")
        print(f"Title: {news[0]['title']}")
        print(f"Summary: {news[0]['summary'][:100]}...")
        print(f"Source: {news[0]['source']} at {news[0]['timestamp']}")
