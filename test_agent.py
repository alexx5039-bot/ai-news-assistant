import asyncio

from app.ai.graph.workflow import graph


async def main():
    async for event in graph.astream(
        {
            "topic": "AI"
        }
    ):
        print(event)


if __name__ == "__main__":
    asyncio.run(main())