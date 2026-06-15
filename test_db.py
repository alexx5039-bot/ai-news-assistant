from sqlalchemy import text

from app.db.database import engine


async def test_connection():
    async with engine.begin() as conn:
        result = await conn.execute(text("SELECT 1"))
        print(result.scalar())


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_connection())