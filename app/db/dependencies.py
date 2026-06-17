from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
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

@asynccontextmanager
async def get_article_service():
    async with AsyncSessionLocal() as session:
        repository = ArticleRepository(session)
        service = ArticleService(repository)

        yield service