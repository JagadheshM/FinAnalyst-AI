"""
FinAnalyst AI – Application Config
Loads environment variables and provides a single config object used across the app.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # LLM
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"

    # Telegram
    telegram_bot_token: str = ""
    telegram_channel_id: str = ""

    # CoinGecko
    coingecko_api_key: str = ""

    # Scheduler
    scheduler_timezone: str = "Asia/Kolkata"
    morning_brief_time: str = "08:45"
    market_wrap_time: str = "15:00"

    # App
    app_env: str = "development"
    log_level: str = "INFO"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
