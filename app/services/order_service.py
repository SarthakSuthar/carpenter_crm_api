from sqlalchemy import update
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.order_schema import (
    OrderCreate,
    OrderLineItemCreate,
    OrderLineItemResponse,
    OrderResponse,
    OrderUpdate,
)


async def create_order(db: AsyncSession, *, order: OrderCreate) -> OrderResponse:

    new_order = OrderCreate(user_id=order.user_id, customer_name=order.customer_name)

    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)

    return OrderResponse.model_validate(new_order)


async def create_new_oreder_item(
    db: AsyncSession, *, order_item: OrderLineItemCreate, order_id: UUID
) -> OrderLineItemResponse:
    new_item = OrderLineItemCreate(
        order_id=order_id,
        item_name=order_item.item_name,
        measurement=order_item.measurement,
        quantity=order_item.quantity,
        rate=order_item.rate,
    )

    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)

    return OrderLineItemResponse.model_validate(new_item)


async def add_item_to_order(*, item_list: list[OrderLineItemResponse]):
    pass
    # TODO: Implement
