from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import AsyncSessionLocal
from app.repositories.article import ArticleRepository
from app.services.article import ArticleService


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


def get_article_repository(
        db: AsyncSession = Depends(get_db),
) -> ArticleRepository:
    return ArticleRepository(db)

def get_article_service(
        repository: ArticleRepository = Depends(
            get_article_repository
        )
) -> ArticleService:
    return ArticleService(repository)