from fastapi import FastAPI
from app.api.routes.article import router as article_router

app = FastAPI()

app.include_router(article_router)
