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
        Generate a highly structured, concise Telegram report for users.
        
        Final Report Structure STRICT TEMPLATE (Follow this exact layout and emojis, do not add extra text, do not write long paragraphs):
        
        📊 *FinAnalyst AI – Daily Brief*
        🗓 Date: {date}
        
        1️⃣ *Top Market News* (Strictly 2–3 bullets max, extremely concise)
        • [News Item 1]
        • [News Item 2]
        
        2️⃣ *Sector Impact* (Short, clear, use arrows ↑ for positive, ↓ for negative, - for neutral)
        • [Sector 1]: [Impact Summary] (e.g. Upstream ↑, Refineries ↓)
        • [Sector 2]: [Impact Summary]
        
        3️⃣ *Key Stocks to Watch* (Symbols or very short names, side by side)
        [Stock1] ↑ | [Stock2] ↑ | [Stock3] ↓ | [Stock4] ↓
        
        4️⃣ *Quick Insights / Recommendations* (Extremely short bullets)
        *Opportunities:*
        ✅ [Opportunity 1]
        ✅ [Opportunity 2]
        *Risks:*
        ⚠️ [Risk 1]
        ⚠️ [Risk 2]
        
        🔔 Stay updated. Always research before investing. Market insights by FinAnalyst AI.
        
        Format the report using Markdown for Telegram. Keep it readable and professional.
        Do not hallucinate. ONLY use the data provided in the Prompt. NEVER write a verbose summary paragraph.
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
        from datetime import datetime
        current_date_str = datetime.now().strftime("%d %b %Y")
        
        chain = prompt | llm
        response = chain.invoke({
            "date": current_date_str,
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
