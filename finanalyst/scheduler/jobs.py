from ..orchestration.graph import app as workflow_app
from ..ui.telegram_bot import push_report_to_telegram
from apscheduler.schedulers.background import BackgroundScheduler
from ..config import get_settings

config = get_settings()

def run_market_briefing():
    """
    The core job function that triggers the entire LangGraph workflow
    and sends the final output to Telegram.
    """
    print("🚀 Triggering FinAnalyst AI Workflow...")
    
    initial_state = {
        "news_articles": [],
        "impactful_news": [],
        "sector_analysis": {},
        "stocks_identified": [],
        "market_data": {},
        "stock_analysis": {},
        "final_report": ""
    }
    
    try:
        # Run graph to completion
        result_state = workflow_app.invoke(initial_state)
        
        final_report = result_state.get("final_report")
        if final_report:
            # Deliver to Telegram
            push_report_to_telegram(final_report)
        else:
            print("❌ Workflow completed but no final report was generated.")
            
    except Exception as e:
        print(f"💥 Critical error during workflow execution: {e}")
        push_report_to_telegram(f"⚠️ *FinAnalyst AI Error:* Failed to execute market briefing.\n`{str(e)}`")

def start_scheduler():
    """
    Initializes and starts the APScheduler.
    """
    scheduler = BackgroundScheduler(timezone=config.scheduler_timezone)
    
    # Parse times from config (e.g. "08:45" -> hour=8, minute=45)
    def parse_time(time_str):
        h, m = time_str.split(":")
        return int(h), int(m)
        
    m_hour, m_minute = parse_time(config.morning_brief_time)
    mw_hour, mw_minute = parse_time(config.market_wrap_time)
    
    # Add jobs
    scheduler.add_job(run_market_briefing, 'cron', day_of_week='mon-fri', hour=m_hour, minute=m_minute, id="morning_brief")
    scheduler.add_job(run_market_briefing, 'cron', day_of_week='mon-fri', hour=mw_hour, minute=mw_minute, id="market_wrap")
    
    scheduler.start()
    print(f"📅 Scheduler started. Next runs scheduled for {config.morning_brief_time} and {config.market_wrap_time} (IST) on weekdays.")
    return scheduler

if __name__ == "__main__":
    import time
    start_scheduler()
    try:
        print("Press Ctrl+C to exit")
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        print("Exiting...")
