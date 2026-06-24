from typing import AsyncGenerator
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

from app.core.security import verify_access_token
from app.db.database import AsyncSessionLocal
from app.db.enums import UserRole
from app.db.models import User
from app.repositories.article import ArticleRepository
from app.repositories.user import UserRepository
from app.services.article import ArticleService
from fastapi.security import OAuth2PasswordBearer

from app.services.user import AuthService


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


def get_article_repository(
        db: AsyncSession = Depends(get_db),
) -> ArticleRepository:
    return ArticleRepository(db)

def get_user_repository(
    db: AsyncSession = Depends(get_db),
) -> UserRepository:
    return UserRepository(db)


def get_article_service(
        repository: ArticleRepository = Depends(
            get_article_repository
        ),
        user_repository: UserRepository = Depends(
            get_user_repository)
) -> ArticleService:

    return ArticleService(repository, user_repository)


def get_auth_service(
    repository: UserRepository = Depends(
        get_user_repository
    )
) -> AuthService:
    return AuthService(repository)

@asynccontextmanager
async def get_article_service_context():
    async with AsyncSessionLocal() as session:
        repository = ArticleRepository(session)
        user_repository = UserRepository(session)
        service = ArticleService(repository, user_repository)

        yield service

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        user_repository: UserRepository = Depends(get_user_repository)
) -> User:

    payload = verify_access_token(token)
    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(status_code=404, detail="Invalid token")

    user = await user_repository.get_user_by_id(int(user_id))

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user

async def get_current_user_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Forbidden")

    return current_user







