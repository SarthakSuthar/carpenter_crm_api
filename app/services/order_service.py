from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order, OrderLineItem, OrderLineNotes
from app.schemas.order_schema import (
    OrderCreate,
    OrderLineItemCreate,
    OrderLineItemResponse,
    OrderNoteCreate,
    OrderNoteResponse,
    OrderResponse,
)


async def get_order(db: AsyncSession, *, order_id: UUID) -> Order:
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    return order


async def create_order(db: AsyncSession, *, order: OrderCreate) -> OrderResponse:

    new_order = Order(user_id=order.user_id, customer_name=order.customer_name)

    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)

    return OrderResponse.model_validate(new_order)


async def delete_order(db: AsyncSession, *, order_id: UUID) -> None:
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    await db.delete(order)
    await db.commit()


async def add_item_to_order(
    db: AsyncSession, *, order_id: UUID, item: OrderLineItemCreate
) -> OrderLineItemResponse:
    order = await get_order(db=db, order_id=order_id)

    new_item = OrderLineItem(
        item_name=item.item_name,
        measurement=item.measurement,
        quantity=item.quantity,
        rate=item.rate,
    )

    order.line_items.append(new_item)
    order.total_amount += new_item.quantity * new_item.rate

    await db.commit()
    await db.refresh(new_item)

    return OrderLineItemResponse.model_validate(new_item)


async def delete_item(db: AsyncSession, *, order_id: UUID, item_id: UUID) -> None:

    item = await db.execute(
        select(OrderLineItem).where(OrderLineItem.order_id == order_id)
    )

    order = await get_order(db=db, order_id=order_id)

    order.line_items.remove(item)


async def add_note_to_order(
    db: AsyncSession, *, order_id: UUID, note: OrderNoteCreate
) -> OrderNoteResponse:
    order = await get_order(db=db, order_id=order_id)

    new_note = OrderLineNotes(order_id=order_id, note=note.note)
    order.notes.append(new_note)

    await db.commit()
    await db.refresh(new_note)

    return OrderNoteResponse.model_validate(new_note)
