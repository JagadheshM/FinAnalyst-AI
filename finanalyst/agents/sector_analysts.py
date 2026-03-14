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

# Helper function to generate an analyst node
def _create_sector_analyst(sector_name: str):
    def analyst_node(state: WorkflowState) -> Dict[str, Any]:
        print(f"--- 🏢 {sector_name} Analyst: Analyzing Sector Impact ---")
        
        impactful_news = state.get("impactful_news", [])
        
        # Filter news relevant strictly to this sector
        sector_news = [
            news for news in impactful_news 
            if sector_name in news.get("affected_sectors", [])
        ]
        
        if not sector_news:
            return {"sector_analysis": {sector_name: []}}
            
        llm = get_llm()
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """
            Role: Sector analysts simulate financial industry analysts specializing in the {sector_name} sector.
            
            Responsibilities:
            • Analyze sector-related news
            • Identify companies that could be impacted
            • Determine positive or negative impact
            • Provide reasoning
            
            Output Format:
            You MUST output ONLY valid JSON. No markdown ```json formatting.
            Return an array of objects formatted exactly like this:
            [
                {{
                    "company": "Company Name",
                    "impact": "Positive/Negative/Neutral",
                    "reason": "Brief reason"
                }}
            ]
            """),
            ("user", "Here is the impactful news for the {sector_name} sector:\n{news_data}\n\nReturn JSON:")
        ])
        
        news_data_str = json.dumps(sector_news, indent=2)
        chain = prompt | llm
        
        try:
            response = chain.invoke({"sector_name": sector_name, "news_data": news_data_str})
            
            content = response.content.strip()
            
            # Very robust stripping of markdown blocks often returned by Gemini
            if "```json" in content:
                content = content.split("```json")[1]
            if "```" in content:
                content = content.split("```")[0]
                
            content = content.strip()
            
            sector_stocks = json.loads(content)
            print(f"✅ {sector_name} Analyst found {len(sector_stocks)} impacted companies.")
            
            return {"sector_analysis": {sector_name: sector_stocks}}
            
        except Exception as e:
            print(f"❌ Error in {sector_name} Analyst: {e}")
            return {"sector_analysis": {sector_name: []}}
            
    return analyst_node

# We must namespace the key correctly in LangGraph when parallel executing,
# so the dict keys are merged rather than overwritten. 
# LangGraph state handles dict merging automatically if the Reducer is configured correctly, 
# but TypedDict normally overwrites. We will use Annotated in State definition to merge dicts later.

technology_analyst_node = _create_sector_analyst("Technology")
banking_analyst_node = _create_sector_analyst("Banking")
energy_analyst_node = _create_sector_analyst("Energy")
automobile_analyst_node = _create_sector_analyst("Automobile")

def merge_stocks_node(state: WorkflowState) -> WorkflowState:
    """
    Synchronizes after the parallel sector analysts and extracts a flat list of unique stocks to research.
    """
    print("--- 🔄 Merging Identified Stocks ---")
    
    sector_analysis = state.get("sector_analysis", {})
    all_stocks = set()
    
    for sector, impacts in sector_analysis.items():
        for impact in impacts:
            company = impact.get("company", "").strip()
            if company:
                # Basic cleaning (e.g., if it outputs TCS (NS:TCS), take TCS)
                all_stocks.add(company)
                
    unique_stocks = list(all_stocks)
    print(f"✅ Identified {len(unique_stocks)} unique stocks across all sectors.")
    
    return {"stocks_identified": unique_stocks}
