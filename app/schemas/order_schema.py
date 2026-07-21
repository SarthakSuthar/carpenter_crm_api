from datetime import datetime
from decimal import Decimal

from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class OrderLineItemBase(BaseModel):
    item_name: str
    measurement: str
    quantity: Decimal = Field(..., ge=0)
    rate: Decimal = Field(..., ge=0)


class OrderLineItemCreate(OrderLineItemBase):
    pass


class OrderLineItemResponse(OrderLineItemBase):
    id: UUID
    order_id: UUID
    model_config = ConfigDict(from_attributes=True)

class OrderNoteBase(BaseModel):
    note: str

class OrderNoteResponse(OrderNoteBase):
    id: UUID
    order_id: UUID
    model_config = ConfigDict(from_attributes=True)
    


class OrderBase(BaseModel):
    customer_name: str
    total_amount: Decimal = Field(..., ge=0)
    notes: list[OrderNoteResponse] = []
    list_item: list[OrderLineItemCreate]


class OrderCreate(OrderBase):
    list_item: list[OrderLineItemCreate]


class OrderUpdate(OrderBase):
    pass


class OrderResponse(OrderBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    line_items: list[OrderLineItemResponse] = []
    notes: list[OrderNoteResponse] = []
    model_config = ConfigDict(from_attributes=True)
