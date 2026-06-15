from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.db.dependencies import get_article_service
from app.db.enums import ArticleStatus
from app.schemas.article import ArticleCreate, ArticleResponse, ArticleUpdate, ArticleStatusUpdate
from app.services.article import ArticleService

router = APIRouter(
    prefix="/articles",
    tags=["Articles"]
)

@router.post("/", response_model=ArticleResponse)
async def create_article(
        article: ArticleCreate,
        service: ArticleService = Depends(get_article_service)
):
    return await service.create_article(article)


@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article(
        article_id: int,
        service: ArticleService = Depends(get_article_service)
):
    return await service.get_article(article_id)


@router.get("/", response_model=list[ArticleResponse])
async def get_articles(
        limit: int = Query(10, ge=1, le=100),
        offset: int = Query(0, ge=0),
        status: ArticleStatus | None = None,
        service: ArticleService = Depends(get_article_service)
):
    return await service.get_articles(
        limit=limit,
        offset=offset,
        status=status
    )

@router.delete("/{article_id}", status_code=204)
async def delete_article(
        article_id: int,
        service: ArticleService = Depends(get_article_service)
):
    await service.delete_article(article_id)

@router.patch("/{article_id}", status_code=200)
async def update_article(
        article_id: int,
        article_data: ArticleUpdate,
        service: ArticleService = Depends(get_article_service)
):
    return await service.update_article(article_id, article_data)

@router.patch("/{article_id}/status")
async def update_status(
        article_id: int,
        status_data: ArticleStatusUpdate,
        service: ArticleService = Depends(get_article_service)
):
    return await service.update_status(
        article_id=article_id,
        status=status_data.status,
    )