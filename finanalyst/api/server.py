from fastapi import FastAPI, BackgroundTasks, HTTPException
from contextlib import asynccontextmanager
from ..scheduler.jobs import start_scheduler, run_market_briefing
from ..config import get_settings

config = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start the background scheduler
    print("Starting FinAnalyst AI Service...")
    scheduler = start_scheduler()
    yield
    # Shutdown: Clean up scheduler
    print("Shutting down FinAnalyst AI Service...")
    scheduler.shutdown()

app = FastAPI(
    title="FinAnalyst AI",
    description="Multi-agent market intelligence system",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "FinAnalyst AI",
        "environment": config.app_env
    }

@app.post("/trigger")
def manual_trigger(background_tasks: BackgroundTasks):
    """
    Manually triggers the LangGraph workflow to run in the background.
    """
    background_tasks.add_task(run_market_briefing)
    return {"message": "Workflow triggered successfully. Check Telegram for the output."}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
