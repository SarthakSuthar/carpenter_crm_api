from decimal import Decimal

from pydantic import BaseModel, Field


class OrderLineItemBase(BaseModel):
    item_name: str
    measurement: str
    quantity: Decimal = Field(..., ge=0)
    rate : Decimal = Field(..., ge=0)

class OrderLineItemCreate(OrderLineItemBase):
    pass    