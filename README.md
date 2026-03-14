# FinAnalyst AI 🤖📈

An **AI-powered multi-agent market intelligence system** that automatically collects financial news, analyzes sector/stock impact, and delivers daily market briefings to a Telegram channel.

## Features
- 📰 **News Collection** – Fetches latest financial news from RSS feeds
- 🔍 **Impact Analysis** – Detects market-relevant events and sentiment
- 🏭 **Sector Analysis** – Parallel agents for Technology, Banking, Energy & Automobile
- 📊 **Market Data** – Live prices, trends, volumes via Yahoo Finance & CoinGecko
- 🤖 **Stock Analysis** – Fundamental, technical, and macro analysis
- 📢 **Telegram Delivery** – Auto-posts briefings at 8:45 AM, 1:00 PM & 6:30 PM IST

## Tech Stack
| Layer | Technology |
|---|---|
| AI Orchestration | LangGraph + LangChain |
| Backend | FastAPI |
| Scheduler | APScheduler |
| Market Data | yfinance, CoinGecko |
| Delivery | Telegram Bot API |
| Deployment | Railway |

## Quick Start

### 1. Clone & Install
```bash
git clone <repo-url>
cd FinAnalyst-AI
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Run Locally
```bash
uvicorn api.server:app --reload
```

### 4. Manual Trigger
```bash
curl -X POST http://localhost:8000/trigger
```

## Project Structure
```
FinAnalyst-AI/
├── agents/
│   ├── news_collector.py       # Fetches & structures news
│   ├── news_impact.py          # Filters impactful news
│   ├── sector_analysts.py      # Parallel sector agents
│   ├── market_data.py          # Market data fetcher agent
│   ├── stock_analysis.py       # Stock analysis agent
│   └── summary_agent.py        # Final report generator
├── orchestration/
│   ├── state.py                # WorkflowState definition
│   └── graph.py                # LangGraph workflow
├── tools/
│   ├── news_scraper.py         # RSS + web scraping
│   └── market_data.py          # yfinance + CoinGecko
├── api/
│   └── server.py               # FastAPI service
├── ui/
│   └── telegram_bot.py         # Telegram delivery
├── scheduler/
│   └── jobs.py                 # APScheduler jobs
├── skills/
│   └── agent_prompts.md        # LLM prompts per agent
├── .env.example
├── requirements.txt
└── Procfile
```

## Deployment
Deploying to Railway is as simple as connecting the GitHub repo. The `Procfile` defines the startup command.

## Supported Assets
- **Indian Stocks** (NSE/BSE equities)
- **Crypto** (Top 10 by market cap)
- **Gold & Silver** (via Yahoo Finance)

## Sectors Covered
Technology | Banking | Energy | Automobile
