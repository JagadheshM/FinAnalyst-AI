import operator
from typing import TypedDict, List, Dict, Any, Annotated

class WorkflowState(TypedDict):
    """
    Shared state for the FinAnalyst AI LangGraph workflow.
    """
    # 1. News Collector Agent Output
    news_articles: List[Dict[str, str]]
    
    # 2. News Impact Analyst Output
    impactful_news: List[Dict[str, Any]]
    
    # 3. Sector Analysts Output
    # Annotated with operator.add (or a custom reducer) to merge sector dicts
    # when parallel agents run concurrently. A dict update reducer is needed.
    
    sector_analysis: Annotated[Dict[str, List[Dict[str, str]]], operator.ior]
    
    # List of unique stocks identified across all sectors
    stocks_identified: List[str]
    
    # 4. Market Data Agent Output
    market_data: Dict[str, Dict[str, Any]]
    
    # 5. Stock Analysis Agent Output
    stock_analysis: Dict[str, Dict[str, str]]
    
    # 6. Investment Summary Agent Output
    final_report: str
