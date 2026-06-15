from __future__ import annotations

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.enums import ArticleStatus
from app.db.models import Article
from app.schemas.article import ArticleCreate


class ArticleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, article_data: ArticleCreate) -> Article:

        article = Article(
            title=article_data.title,
            content=article_data.content
        )
        self.db.add(article)

        await self.db.commit()
        await self.db.refresh(article)

        return article


    async def get_article_by_id(self, article_id: int) -> Article | None:
        return await self.db.get(
            Article,
            article_id,
        )

    async def get_articles(self,
                           limit: int = 10,
                           offset: int = 0,
                           status: ArticleStatus | None = None
    ) -> Sequence[Article]:

        query = select(Article)
        if status:
            query = query.where(
                Article.status == status
            )
        query = query.offset(offset).limit(limit)

        result = await self.db.execute(query)

        return result.scalars().all()


    async def delete_article(self, article: Article):

        await self.db.delete(article)
        await self.db.commit()


    async def update_article(self, article: Article):

        await self.db.commit()
        await self.db.refresh(article)
        return article