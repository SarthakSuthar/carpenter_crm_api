import uuid
from datetime import datetime

from models.base import Base
from models.order import Order
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    user_name: Mapped[str] = mapped_column(String(255))
    company_name: Mapped[str | None] = mapped_column(String(255), default=None)
    contact_person_name: Mapped[str | None] = mapped_column(String(255), default=None)
    contact_number: Mapped[str | None] = mapped_column(String(255), default=None)
    address: Mapped[str | None] = mapped_column(String(255), default=None)
    company_logo: Mapped[str | None] = mapped_column(String(255), default=None)
    orders: Mapped[list["Order"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
