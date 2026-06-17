from __future__ import annotations

from typing_extensions import TypedDict


class ArticleState(TypedDict):
    topic: str
    news: str
    title: str
    content: str
    article_id: int | None