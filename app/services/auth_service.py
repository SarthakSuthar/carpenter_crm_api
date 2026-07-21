
from fastapi import HTTPException, status
from sqlalchemy import  exists, select,update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decrypt_password, get_password_hash
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserResponse


async def create_user(db: AsyncSession,*, user: UserCreate ) -> UserResponse  : 

    check_user_exist = await db.execute(select(exists().where(User.email == user.email)))
    if check_user_exist.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
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


async def authenticate_user(db: AsyncSession,*, email: str, hashed_password: str) -> UserResponse | None :

    result =  await db.execute(select(User).where(User.email == email ).limit(1))
    user = result.scalar_one_or_none()

    if user is None or not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    return UserResponse.model_validate(user)


async def reset_password(db : AsyncSession, *, email: str, hashed_new_password:str) -> str :

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user is None:
         raise HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email does not exist",
            )
           
    old_password = user.hashed_password

    if (decrypt_password(hashed_new_password) == decrypt_password(old_password)):
         return "New password can not be same as old password."
        
    await db.execute(update(User.hashed_password).where(User.email == email))
    await db.commit()
    await db.refresh(user)

    return "Password updated successfully."