from api.dependencies import get_db
from fastapi import APIRouter, Depends
from schemas.user_schema import UserResponse, UserUpdate
from services.auth_service import update_profile
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/user", tags=["user"])


@router.patch("/{user_id}", response_model=UserResponse)
async def update_profile_data(db: AsyncSession = Depends(get_db), *, body: UserUpdate):
    return await update_profile(db=db, data=body)
