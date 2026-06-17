from fastapi import APIRouter

from app.ai.graph.workflow import graph
from app.schemas.article import (
    GenerateArticleRequest,
    GenerateArticleResponse
)

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)

@router.post(
    "/generate-article",
    response_model=GenerateArticleResponse
)
async def generate_article(
        request: GenerateArticleRequest
):
    result = await graph.ainvoke(
        {
            "topic": request.topic
        }
    )
    return GenerateArticleResponse(
        article_id=result["article_id"],
        topic=result["topic"]
    )
