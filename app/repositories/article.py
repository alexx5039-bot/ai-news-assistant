from __future__ import annotations

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.enums import ArticleStatus
from app.db.models import Article, ArticleSource
from app.schemas.article import ArticleCreate


class ArticleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, article_data: ArticleCreate, author_id: int) -> Article:

        article = Article(
            title=article_data.title,
            content=article_data.content,
            author_id=author_id

        )
        self.db.add(article)

        await self.db.commit()
        await self.db.refresh(article)

        return await self.get_article_by_id(article.id)

    async def get_article_by_id(
            self,
            article_id: int
    ) -> Article | None:
        result = await self.db.execute(
            select(Article)
            .options(
                selectinload(Article.sources)
            )
            .where(
                Article.id == article_id
            )
        )

        return result.scalar_one_or_none()

    async def get_articles(self,
                           limit: int = 10,
                           offset: int = 0,
                           status: ArticleStatus | None = None
    ) -> Sequence[Article]:

        query = select(Article).options(selectinload(Article.sources))
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


    async def create_source(
        self,
        article_id: int,
        title: str,
        url: str
    ) -> ArticleSource:

        source = ArticleSource(
            article_id=article_id,
            title=title,
            url=url
        )

        self.db.add(source)

        await self.db.commit()
        await self.db.refresh(source)

        return source