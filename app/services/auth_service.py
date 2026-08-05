from core.security import get_password_hash, verify_password
from fastapi import HTTPException, status
from models.user import User
from schemas.user_schema import UserCreate, UserResponse, UserUpdate
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession


# MARK: Sign Up method
async def create_user(db: AsyncSession, *, user: UserCreate) -> UserResponse:
    exists_result = await db.execute(select(exists().where(User.email == user.email)))
    if exists_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    hashed_password = get_password_hash(user.password)

    new_user = User(
        email=user.email,
        user_name=user.user_name,
        hashed_password=hashed_password,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return UserResponse.model_validate(new_user)


# MARK: Sign in method
async def authenticate_user(
    db: AsyncSession, *, email: str, password: str
) -> UserResponse | None:

    result = await db.execute(select(User).where(User.email == email).limit(1))
    user = result.scalar_one_or_none()

    if user is None or not verify_password(
        plain_password=password, hashed_password=user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    return UserResponse.model_validate(user)


# MARK: Reset Password
async def reset_password(db: AsyncSession, *, email: str, new_password: str) -> str:

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email does not exist",
        )

    if verify_password(
        plain_password=new_password, hashed_password=user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password cannot be the same as the old password.",
        )

    user.hashed_password = get_password_hash(new_password)
    await db.commit()
    await db.refresh(user)

    return "Password updated successfully."


# MARK: Update Profile
async def update_profile(db: AsyncSession, *, data: UserUpdate) -> UserResponse:
    result = await db.execute(select(User).where(User.id == data.id))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    user.company_name = data.company_name
    user.contact_number = data.contact_number
    user.contact_person_name = data.contact_person_name
    user.address = data.address
    user.company_logo = data.company_logo

    await db.commit()
    await db.refresh(user)

    return UserResponse.model_validate(user)
