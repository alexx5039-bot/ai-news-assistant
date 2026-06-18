from fastapi import FastAPI
from app.api.routes.article import router as article_router
from app.api.routes.chat import router as chat_router
from app.api.routes.ai import router as ai_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(article_router)
app.include_router(chat_router)
app.include_router(ai_router)
