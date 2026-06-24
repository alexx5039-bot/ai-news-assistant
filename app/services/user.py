from __future__ import annotations

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import hash_password, verify_password, create_access_token
from app.db.models import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, LoginRequest


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def register(self, user_data: UserCreate) -> User:

        existing_user = await self.repository.get_user_by_email(
            user_data.email
        )
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already exists")
        hashed_password = hash_password(user_data.password)

        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )
        return await self.repository.create_user(user)

    async def login(
            self,
            form_data: OAuth2PasswordRequestForm
    ) -> dict:

        user = await self.repository.get_user_by_email(
            form_data.username
        )

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        if not verify_password(
                form_data.password,
                user.hashed_password
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        token = create_access_token(
            {"sub": str(user.id)}
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    async def get_user_by_id(self, user_id) -> User | None:
        user = await self.repository.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def get_user_by_email(self, email) -> User | None:
        user = await self.repository.get_user_by_email(email)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
