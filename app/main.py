from fastapi import FastAPI
from app.api.routes.article import router as article_router
from app.api.routes.chat import router as chat_router
from app.api.routes.ai import router as ai_router

app = FastAPI()

app.include_router(article_router)
app.include_router(chat_router)
app.include_router(ai_router)
