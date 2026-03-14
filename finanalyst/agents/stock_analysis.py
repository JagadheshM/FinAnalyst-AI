import json
from typing import Dict, Any, List
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

def stock_analysis_node(state: WorkflowState) -> WorkflowState:
    """
    Agent 5: Stock Analysis Agent
    Takes fetched market data and sector analysis insights to output a comprehensive stock view.
    """
    print("--- 🧠 Stock Analysis Agent: Analyzing Equities & Crypto ---")
    
    market_data = state.get("market_data", {})
    sector_analysis = state.get("sector_analysis", {})
    
    if not market_data:
        print("No market data to analyze.")
        return {"stock_analysis": {}}
        
    # Build a combined context string for the LLM
    context_str = "Market Data:\n"
    context_str += json.dumps(market_data, indent=2) + "\n\n"
    
    context_str += "Sector Analysis (Why these stocks were picked):\n"
    for sector, impacts in sector_analysis.items():
        if impacts:
            context_str += f"- {sector}:\n"
            for imp in impacts:
                context_str += f"  {imp.get('company')}: {imp.get('impact')} - {imp.get('reason')}\n"
    
    llm = get_llm()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        Role: Perform financial analysis on each stock.
        
        Analysis Types:
        Fundamental Analysis
        - Revenue growth
        - Profit margin
        - Market capitalization
        
        Technical Analysis
        - Price trend
        - Momentum
        - Support/resistance signals
        
        Market Sentiment
        - News sentiment
        - Investor interest
        
        Industry Position
        - Market leadership
        - Competitive advantage
        
        Macro Impact
        - Interest rates
        - Inflation
        - Government policy
        
        Output Format:
        You MUST output ONLY valid JSON. Return a dictionary object keyed by the stock symbol.
        No markdown ```json formatting.
        
        {{
            "SYMBOL1": {{
                "fundamental": "String",
                "technical": "String",
                "sentiment": "String",
                "industry_position": "String",
                "macro_outlook": "String"
            }},
            "SYMBOL2": ...
        }}
        """),
        ("user", "Here is the raw data and context:\n{context_str}\n\nReturn JSON:")
    ])
    
    chain = prompt | llm
    
    try:
        response = chain.invoke({"context_str": context_str})
        
        content = response.content.strip()
        
        # Very robust stripping of markdown blocks often returned by Gemini
        if "```json" in content:
            content = content.split("```json")[1]
        if "```" in content:
            content = content.split("```")[0]
            
        content = content.strip()
        
        analysis = json.loads(content)
        print(f"✅ Analyzed {len(analysis)} stocks.")
        
        return {"stock_analysis": analysis}
        
    except Exception as e:
        print(f"❌ Error in Stock Analysis Agent: {e}")
        return {"stock_analysis": {}}
