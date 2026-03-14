from ..orchestration.state import WorkflowState
from ..tools.news_scraper import collect_latest_news

def news_collector_node(state: WorkflowState) -> WorkflowState:
    """
    Agent 1: News Collector
    Fetches the latest financial news and populates the state.
    """
    print("--- 📰 News Collector Agent: Fetching News ---")
    
    # Collect news from RSS feeds
    articles = collect_latest_news()
    
    print(f"✅ Collected {len(articles)} unique news items.")
    
    # Update state
    return {"news_articles": articles}
