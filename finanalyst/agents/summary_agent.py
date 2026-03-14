def summary_agent_node(state: dict) -> dict:
    from langchain_core.prompts import ChatPromptTemplate
    from .news_impact import get_llm
    
    print("--- 📝 Summary Agent: Generating Final Post ---")
    
    llm = get_llm()
    
    # Extract pieces directly from state
    news = state.get("impactful_news", [])
    sector = state.get("sector_analysis", {})
    stocks = state.get("stocks_identified", [])
    analysis = state.get("stock_analysis", {})
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        Role: Generate the final market intelligence report.
        
        Responsibilities:
        Combine outputs from all agents.
        Generate a structured report for users.
        
        Final Report Structure:
        
        # 📊 FinAnalyst Daily Brief
        
        ## 1. News Summary
        Key market-moving events.
        
        ## 2. Sector Impact
        Which sectors are affected and why.
        
        ## 3. Stocks to Watch
        List of companies impacted by news.
        
        ## 4. Stock Analysis
        Key insights about each stock.
        
        ## 5. AI Investment Insights
        Potential opportunities and risks.
        
        Format the report using Markdown for Telegram. Keep it readable and professional.
        Do not hallucinate. ONLY use the data provided in the Prompt.
        """),
        ("user", """
        Raw Data for the Briefing:
        Impactful News: {news}
        Sector Impacts: {sector}
        Stocks Identified: {stocks}
        Stock Analysis: {analysis}
        
        Write the Telegram post:
        """)
    ])
    
    try:
        chain = prompt | llm
        response = chain.invoke({
            "news": news,
            "sector": sector,
            "stocks": stocks,
            "analysis": analysis
        })
        report = response.content.strip()
        print("✅ FinAnalyst Daily Brief generated.")
        return {"final_report": report}
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        return {"final_report": "Error generating FinAnalyst brief at this time. Please check logs."}
