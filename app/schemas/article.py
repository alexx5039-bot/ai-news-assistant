from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.db.enums import ArticleStatus

class ArticleCreate(BaseModel):
    title: str
    content: str

class ArticleSourceResponse(BaseModel):
    id: int
    title: str
    url: str

    model_config = ConfigDict(from_attributes=True)

class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    status: ArticleStatus
    created_at: datetime
    sources: list[ArticleSourceResponse] = []

    model_config = ConfigDict(
        from_attributes=True
    )

class ArticleUpdate(BaseModel):
    title: str | None = None
    content: str | None = None

class ArticleStatusUpdate(BaseModel):
    status: ArticleStatus

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str

class GenerateArticleRequest(BaseModel):
    topic: str

class GenerateArticleResponse(BaseModel):
    article_id: int
    topic: str

class ReviewResponse(BaseModel):
    score: int = Field(ge=1, le=10)

class ArticleSourceCreate(BaseModel):
    article_id: int
    title: str
    url: str