from __future__ import annotations

from typing_extensions import TypedDict


class ArticleState(TypedDict):
    topic: str
    news: str
    title: str
    content: str
    sources: list[dict]
    summary: str
    quality_score: int
    review_attempts: int
    article_id: int | None