import asyncio
from finanalyst.orchestration.graph import run_pipeline


async def main():
    print("🚀 Starting FinAnalyst AI pipeline...")

    result = await run_pipeline()

    print("✅ Pipeline completed")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())