import asyncio

from app.ai.graph.workflow import graph


async def main():
    result = await graph.ainvoke(
        {
            "topic": "Artificial Intelligence"
        }
    )

    print("FINAL STATE:")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())