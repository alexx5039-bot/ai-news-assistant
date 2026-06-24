from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
import json

from app.ai.graph.workflow import graph
from app.db.dependencies import get_current_user
from app.db.models import User
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
        request: GenerateArticleRequest,
        current_user: User = Depends(get_current_user)
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



@router.post("/generate-article-stream")
async def generate_article_stream(
        request: GenerateArticleRequest,
        current_user: User = Depends(get_current_user)
):
    async def event_generator():

        async for event in graph.astream(
                {
                    "topic": request.topic
                }
        ):
            node_name = list(event.keys())[0]

            yield (
                f"data: {json.dumps({'node': node_name})}\n\n"
            )

        yield (
            f"data: {json.dumps({'status': 'completed'})}\n\n"
        )

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )