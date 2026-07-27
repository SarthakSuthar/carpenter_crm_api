from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from uuid import UUID


class UserCreate(BaseModel):
    user_name: str
    email: EmailStr
    password: str = Field(
        ..., min_length=6, description="Password must be at least 6 characters long"
    )


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    id: UUID
    company_name: str | None = None
    contact_person_name: str | None = None
    contact_number: str | None = None
    address: str | None = None
    company_logo: str | None = None


class UserResponse(BaseModel):
    id: UUID
    user_name: str
    email: EmailStr
    company_name: str | None = None
    contact_person_name: str | None = None
    contact_number: str | None = None
    address: str | None = None
    company_logo: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
