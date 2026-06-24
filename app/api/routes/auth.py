from fastapi import APIRouter, Depends
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from app.db.dependencies import get_auth_service, get_current_user
from app.db.models import User
from app.schemas.user import UserResponse, UserCreate, TokenResponse, LoginRequest
from app.services.user import AuthService

router = APIRouter()

@router.get("/me")
async def me(
    current_user: User = Depends(
        get_current_user
    )
):
    return current_user


@router.post("/register",
             response_model=UserResponse,
             status_code=status.HTTP_201_CREATED
             )
async def register(user_data: UserCreate,
                   service: AuthService = Depends(get_auth_service)
                   ):

    return await service.register(user_data)


@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                service: AuthService = Depends(get_auth_service)
                ):

    return await service.login(form_data)