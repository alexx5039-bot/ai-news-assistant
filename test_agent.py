import asyncio

from app.ai.agent import agent


async def main():
    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Search for latest AI news, create an article from them and save it"
                }
            ]
        }
    )

    for message in result["messages"]:
        print(type(message).__name__)

        if hasattr(message, "tool_calls") and message.tool_calls:
            for tool_call in message.tool_calls:
                print(f"Tool: {tool_call['name']}")
                print(f"Args: {tool_call['args']}")

        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(main())