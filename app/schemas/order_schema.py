from datetime import datetime
from decimal import Decimal

from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


# MARK: Order Line
class OrderLineItemCreate(BaseModel):
    item_name: str
    order_id: UUID
    measurement: str
    quantity: Decimal = Field(..., ge=0)
    rate: Decimal = Field(..., ge=0)


class OrderLineItemUpdate(BaseModel):
    id: UUID
    order_id: UUID
    item_name: str
    measurement: str
    quantity: Decimal = Field(..., ge=0)
    rate: Decimal = Field(..., ge=0)


class OrderLineItemResponse(BaseModel):
    id: UUID
    order_id: UUID
    item_name: str
    measurement: str
    quantity: Decimal = Field(..., ge=0)
    rate: Decimal = Field(..., ge=0)
    model_config = ConfigDict(from_attributes=True)


# MARK: Order Note


class OrderNoteCreate(BaseModel):
    note: str
    order_id: UUID


class OrderNoteUpdate(BaseModel):
    note: str
    id: UUID


class OrderNoteResponse(BaseModel):
    id: UUID
    order_id: UUID
    model_config = ConfigDict(from_attributes=True)


# MARK: Order
class OrderCreate(BaseModel):
    user_id: UUID
    customer_name: str


class OrderUpdate(BaseModel):
    id: UUID
    user_id: UUID
    customer_name: str
    line_items: list[OrderLineItemResponse] = []
    notes: list[OrderNoteResponse] = []
    created_at: datetime
    updated_at: datetime


class OrderResponse(BaseModel):
    id: UUID
    user_id: UUID
    customer_name: str
    line_items: list[OrderLineItemResponse] = []
    notes: list[OrderNoteResponse] = []
    total_amount: Decimal = Field(..., ge=0)
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
