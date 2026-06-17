from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.db.enums import ArticleStatus

class ArticleCreate(BaseModel):
    title: str
    content: str

class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    status: ArticleStatus
    created_at: datetime

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

