from fastapi import APIRouter, Depends

from app.ai.agent import agent
from app.db.dependencies import get_current_user
from app.db.models import User
from app.schemas.article import (
    ChatRequest,
    ChatResponse,
)

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post(
    "/chat",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest

) -> ChatResponse:

    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": request.message,
                }
            ]
        }
    )

    response = result["messages"][-1].content

    return ChatResponse(
        response=response,
    )