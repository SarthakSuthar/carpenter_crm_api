from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order, OrderLineItem, OrderLineNotes
from app.schemas.order_schema import (
    OrderCreate,
    OrderLineItemCreate,
    OrderLineItemResponse,
    OrderLineItemUpdate,
    OrderNoteCreate,
    OrderNoteResponse,
    OrderNoteUpdate,
    OrderResponse,
)


# MARK: Order
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


# MARK: Items
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


async def update_item(
    db: AsyncSession, *, order_id: UUID, item_id: UUID, item: OrderLineItemUpdate
) -> OrderLineItemResponse:
    order = await get_order(db=db, order_id=order_id)

    result = await db.execute(
        select(OrderLineItem).where(
            OrderLineItem.id == item_id, OrderLineItem.order_id == order_id
        )
    )

    item_result = result.scalar_one_or_none()

    if item_result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Line item not found",
        )

    item_result.item_name = item.item_name if item.item_name else item_result.item_name
    item_result.measurement = (
        item.measurement if item.measurement else item_result.measurement
    )
    item_result.quantity = item.quantity if item.quantity else item_result.quantity
    item_result.rate = item.rate if item.rate else item_result.rate

    for i in order.line_items:
        order.total_amount += i.quantity * i.rate

    await db.commit()
    await db.refresh(item_result)

    return OrderLineItemResponse.model_validate(item_result)


async def delete_item(db: AsyncSession, *, order_id: UUID, item_id: UUID) -> None:
    order = await get_order(db=db, order_id=order_id)

    result = await db.execute(
        select(OrderLineItem).where(
            OrderLineItem.id == item_id, OrderLineItem.order_id == order_id
        )
    )
    item = result.scalar_one_or_none()

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Line item not found",
        )

    order.line_items.remove(item)
    order.total_amount -= item.quantity * item.rate

    await db.commit()


# MARK: Notes
async def add_note_to_order(
    db: AsyncSession, *, order_id: UUID, note: OrderNoteCreate
) -> OrderNoteResponse:
    order = await get_order(db=db, order_id=order_id)

    new_note = OrderLineNotes(order_id=order_id, note=note.note)
    order.notes.append(new_note)

    await db.commit()
    await db.refresh(new_note)

    return OrderNoteResponse.model_validate(new_note)


async def update_note(
    db: AsyncSession, *, order_id: UUID, note_id: UUID, note: OrderNoteUpdate
) -> OrderNoteResponse:

    result = await db.execute(
        select(OrderLineNotes).where(
            OrderLineNotes.id == note_id, OrderLineNotes.order_id == order_id
        )
    )

    note_result = result.scalar_one_or_none()

    if note_result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    note_result.note = note.note if note.note else note_result.note

    await db.commit()
    await db.refresh(note_result)

    return OrderNoteResponse.model_validate(note_result)


async def delete_note(db: AsyncSession, *, order_id: UUID, note_id: UUID) -> None:
    order = await get_order(db=db, order_id=order_id)

    result = await db.execute(
        select(OrderLineNotes).where(
            OrderLineNotes.id == note_id, OrderLineNotes.order_id == order_id
        )
    )

    note = result.scalar_one_or_none()

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    order.notes.remove(note)

    await db.commit()
