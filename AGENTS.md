# FinAnalyst AI – Agent Definitions

This document defines the behavior, responsibilities, inputs, and outputs of each AI agent used in the FinAnalyst AI multi-agent system.

Agents are orchestrated using LangGraph and share a common workflow state.

---

# Shared Workflow State

All agents read and write to a shared state object.

State fields:

news_articles
impactful_news
sector_analysis
stocks_identified
market_data
stock_analysis
final_report

---

# 1. News Collector Agent

## Role

Collect the latest financial and macroeconomic news that could influence markets.

## Responsibilities

• Fetch latest news articles
• Extract headline, summary, timestamp, and source
• Remove duplicate articles
• Normalize article format

## News Types to Collect

• Corporate announcements
• Government policy announcements
• Geopolitical events
• Technology breakthroughs
• Fraud or regulatory actions
• Earnings announcements

## Output Format

```
news_articles = [
{
title: "",
summary: "",
source: "",
timestamp: "",
category: ""
}
]
```

---

# 2. News Impact Analyst

## Role

Determine which news events are relevant to financial markets.

## Responsibilities

• Analyze collected news
• Identify news that may affect markets
• Determine sentiment (positive / negative / neutral)
• Map news to impacted sectors

## Sector Categories

Technology
Banking
Energy
Automobile

## Output Format

```
impactful_news = [
{
news_title: "",
summary: "",
sentiment: "",
affected_sectors: []
}
]
```

---

# 3. Sector Analyst Agents

Sector analysts simulate financial industry analysts.

Agents:

Technology Analyst
Banking Analyst
Energy Analyst
Automobile Analyst

These agents run **in parallel**.

---

## Responsibilities

• Analyze sector-related news
• Identify companies that could be impacted
• Determine positive or negative impact
• Provide reasoning

---

## Example

News:

Government announces EV subsidy.

Automobile Analyst Output:

```
sector_analysis = {
sector: "Automobile",
stocks: [
{
company: "Tata Motors",
impact: "Positive",
reason: "EV subsidy boosts EV demand"
}
]
}
```

---

# 4. Market Data Agent

## Role

Fetch financial data for all identified stocks.

## Responsibilities

• Fetch latest stock price
• Fetch recent price trend
• Fetch trading volume
• Fetch key indicators

Assets supported

Indian equities
Crypto
Gold
Silver

---

## Output Format

```
market_data = {
"TCS": {
price: "",
trend: "",
volume: ""
}
}
```

---

# 5. Stock Analysis Agent

## Role

Perform financial analysis on each stock.

---

## Analysis Types

Fundamental Analysis

Revenue growth
Profit margin
Market capitalization

Technical Analysis

Price trend
Momentum
Support/resistance signals

Market Sentiment

News sentiment
Investor interest

Industry Position

Market leadership
Competitive advantage

Macro Impact

Interest rates
Inflation
Government policy

---

## Output Format

```
stock_analysis = {
"TCS": {
fundamental: "",
technical: "",
sentiment: "",
industry_position: "",
macro_outlook: ""
}
}
```

---

# 6. Investment Summary Agent

## Role

Generate the final market intelligence report.

---

## Responsibilities

Combine outputs from all agents.

Generate a structured report for users.

---

## Final Report Structure

1. News Summary

Key market-moving events.

2. Sector Impact

Which sectors are affected and why.

3. Stocks to Watch

List of companies impacted by news.

4. Stock Analysis

Key insights about each stock.

5. AI Investment Insights

Potential opportunities and risks.

---

# Communication Rules

Agents must:

• Only read required state fields
• Only write their assigned output field
• Avoid modifying other agent outputs

---

# Execution Order

1. News Collector Agent
2. News Impact Analyst
3. Sector Analysts (parallel)
4. Merge identified stocks
5. Market Data Agent
6. Stock Analysis Agent
7. Investment Summary Agent
