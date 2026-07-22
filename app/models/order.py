from datetime import datetime
from decimal import Decimal
import uuid

from sqlalchemy import DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.user import User


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.UUID )
    user: Mapped["User"] = relationship(back_populates="orders")
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    customer_name: Mapped[str] = mapped_column(String(255))
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10,2), default=0.00)
    notes: Mapped[list["NotesItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")
    line_items : Mapped[list["OrderLineItem"]] = relationship(back_populates="order", cascade="all, delete-orphan"
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
    )

class OrderLineItem(Base):
    __tablename__ = "order_line_items"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.UUID )
    order_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), index=True)
    item_name: Mapped[str] = mapped_column(String(255))
    measurement: Mapped[str] = mapped_column(String(60))
    quantity: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    rate: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    order: Mapped["Order"] = relationship(back_populates="line_items")


class NotesItem(Base):
    __tablename__ = "notes_items"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.UUID )
    order_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), index=True)
    note: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    order: Mapped["Order"] = relationship(back_populates="notes")