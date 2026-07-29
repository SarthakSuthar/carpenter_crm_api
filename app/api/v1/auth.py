from fastapi import APIRouter
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user_schema import UserCreate, UserLogin, UserResponse
from app.services.auth_service import authenticate_user, create_user, reset_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=UserResponse)
async def login(
    db: AsyncSession = Depends(get_db), *, user: UserLogin
) -> UserResponse | None:
    return await authenticate_user(db=db, email=user.email, password=user.password)


@router.post("/signup", response_model=UserResponse)
async def sign_up(
    db: AsyncSession = Depends(get_db), *, user: UserCreate
) -> UserResponse:
    return await create_user(db=db, user=user)


@router.post("/forgot-password", status_code=200)
async def forgot_password(
    db: AsyncSession = Depends(get_db), *, email: EmailStr, password: str
) -> str:
    return await reset_password(db=db, email=email, new_password=password)
