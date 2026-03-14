import json
from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from ..orchestration.state import WorkflowState
from ..config import get_settings

config = get_settings()

def get_llm():
    return ChatGoogleGenerativeAI(
        model=config.gemini_model, 
        google_api_key=config.gemini_api_key, 
        temperature=0.1
    )

def news_impact_node(state: WorkflowState) -> WorkflowState:
    """
    Agent 2: News Impact Analyst
    Analyzes collected news to find market-impacting events and their sentiment.
    """
    print("--- 🧐 News Impact Analyst: Filtering & Analyzing ---")
    
    news_articles = state.get("news_articles", [])
    if not news_articles:
        print("No news to process.")
        return {"impactful_news": []}
    
    llm = get_llm()
    
    # Prompt explicitly enforcing valid JSON
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        Role: Determine which news events are relevant to financial markets.
        
        Responsibilities:
        • Analyze collected news
        • Identify news that may affect markets
        • Determine sentiment (positive / negative / neutral)
        • Map news to impacted sectors
        
        Sector Categories:
        Technology, Banking, Energy, Automobile
        
        Output Format:
        You MUST output ONLY valid JSON. Your response must be an array of objects.
        No markdown formatting block like ```json ... ```, just the raw JSON text.
        
        [
            {{
                "news_title": "String",
                "summary": "String",
                "sentiment": "String",
                "affected_sectors": ["String"]
            }}
        ]
        """),
        ("user", "Here is the raw news data:\n{news_data}\n\nAnalyze and return the JSON array of impactful news:")
    ])
    
    # Format inputs for LLM
    news_data_str = json.dumps(news_articles, indent=2)
    chain = prompt | llm
    
    try:
        response = chain.invoke({"news_data": news_data_str})
        
        # Clean response content (strip markdown if model still included it)
        content = response.content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
            
        impactful_news = json.loads(content.strip())
        print(f"✅ Identified {len(impactful_news)} impactful news events out of {len(news_articles)}.")
        return {"impactful_news": impactful_news}
        
    except Exception as e:
        print(f"❌ Error in News Impact Analyst: {e}")
        return {"impactful_news": []}
