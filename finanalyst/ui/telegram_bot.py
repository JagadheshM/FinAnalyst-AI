import asyncio
from telegram import Bot
from telegram.constants import ParseMode
from ..config import get_settings

config = get_settings()

async def send_telegram_message(message: str) -> bool:
    """
    Sends a formatted Markdown message to the configured Telegram channel.
    Splits message if it exceeds the length limit.
    """
    if not config.telegram_bot_token or not config.telegram_channel_id:
        print("Telegram credentials not configured. Skipping message delivery.")
        # Print to console for local debugging if no token is provided
        print("--- TARGET MESSAGE ---")
        print(message)
        print("----------------------")
        return False
        
    try:
        bot = Bot(token=config.telegram_bot_token)
        
        # Telegram max message length is 4096
        MAX_LENGTH = 4000
        parts = [message[i:i+MAX_LENGTH] for i in range(0, len(message), MAX_LENGTH)]
        
        for part in parts:
            try:
                await bot.send_message(
                    chat_id=config.telegram_channel_id,
                    text=part,
                    parse_mode=ParseMode.MARKDOWN
                )
            except Exception as e:
                print(f"⚠️ Markdown parsing failed, sending as plain text: {e}")
                # Fallback to plain text if markdown is broken
                await bot.send_message(
                    chat_id=config.telegram_channel_id,
                    text=part
                )
        
        print(f"✅ Message sent to Telegram in {len(parts)} part(s).")
        return True
    except Exception as e:
        print(f"❌ Failed to send Telegram message: {e}")
        return False

def push_report_to_telegram(report: str):
    """
    Synchronous wrapper to run the async Telegram send function.
    Useful for running within synchronous APScheduler or LangGraph flows.
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # Running inside an existing event loop (like FastAPI)
        asyncio.create_task(send_telegram_message(report))
    else:
        # Running in a standalone sync thread
        asyncio.run(send_telegram_message(report))

if __name__ == "__main__":
    # Quick test
    push_report_to_telegram("🛠 *Test Message* from FinAnalyst AI")
