from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr
from sqlalchemy import UUID


class UserBase(BaseModel):
    user_id: str
    user_name: str
    email: EmailStr
    company_name: str | None
    contact_person_name : str | None
    contact_number: str | None = None
    address: str | None = None
    company_logo: str | None = None


class UserCreate(UserBase):
    google_id: str

class UserUpdate(BaseModel):
    company_name: str | None = None
    contact_person_name: str | None = None
    contact_number: str | None = None
    address: str | None = None
    company_logo: str | None = None

class UserResponse(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)