from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy import UUID


class UserBase(BaseModel):
    user_id: str
    user_name: str
    email: EmailStr
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters long")
    company_name: str | None
    contact_person_name : str | None
    contact_number: str | None = None
    address: str | None = None
    company_logo: str | None = None

class UserLogin(UserBase):
    email: str
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters long")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters long")

class UserUpdate(BaseModel):
    company_name: str | None = None
    contact_person_name: str | None = None
    contact_number: str | None = None
    address: str | None = None
    company_logo: str | None = None

class UserResponse(UserBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)