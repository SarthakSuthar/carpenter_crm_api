from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db
from app.schemas.order_schema import (
    OrderCreate,
    OrderLineItemCreate,
    OrderLineItemResponse,
    OrderLineItemUpdate,
    OrderNoteCreate,
    OrderNoteResponse,
    OrderNoteUpdate,
    OrderResponse,
    OrderUpdate,
)
from app.services.order_service import (
    add_item_to_order,
    add_note_to_order,
    create_order,
    delete_item,
    delete_note_to_order,
    delete_order,
    get_order,
    get_order_list_by_user_id,
    update_item_to_order,
    update_note_to_order,
    update_order,
)

router = APIRouter(prefix="/orders", tags=["order"])


# MARK: Orders
@router.get("/{order_id}", response_model=OrderResponse)
async def get_order_by_id(
    order_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    return await get_order(db=db, order_id=order_id)


@router.get("", response_model=list[OrderResponse])
async def get_order_list(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    return await get_order_list_by_user_id(db=db, user_id=user_id)


@router.post("", response_model=OrderResponse)
async def create_new_order(
    body: OrderCreate,
    db: AsyncSession = Depends(get_db),
):
    return await create_order(db=db, order=body)


@router.patch("/{order_id}", response_model=OrderResponse)
async def update_order_by_id(
    order_id: UUID,
    body: OrderUpdate,
    db: AsyncSession = Depends(get_db),
) -> OrderResponse:
    return await update_order(db=db, order_id=order_id, order=body)


@router.delete("/{order_id}")
async def delete_order_by_id(
    order_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    return await delete_order(db=db, order_id=order_id)


# MARK: Items
@router.post("/{order_id}/items", response_model=OrderLineItemResponse)
async def add_new_item(
    order_id: UUID,
    item: OrderLineItemCreate,
    db: AsyncSession = Depends(get_db),
):
    return await add_item_to_order(db=db, order_id=order_id, item=item)


@router.patch("/{order_id}/items/{item_id}", response_model=OrderLineItemResponse)
async def update_item(
    order_id: UUID,
    item_id: UUID,
    item: OrderLineItemUpdate,
    db: AsyncSession = Depends(get_db),
):
    return await update_item_to_order(
        db=db, order_id=order_id, item_id=item_id, item=item
    )


@router.delete("/{order_id}/items/{item_id}")
async def delete_item_by_id(
    order_id: UUID,
    item_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    return await delete_item(db=db, order_id=order_id, item_id=item_id)


# MARK: Notes
@router.post("/{order_id}/notes", response_model=OrderNoteResponse)
async def add_note(
    order_id: UUID,
    note: OrderNoteCreate,
    db: AsyncSession = Depends(get_db),
):
    return await add_note_to_order(db=db, order_id=order_id, note=note)


@router.patch("/{order_id}/notes/{note_id}", response_model=OrderNoteResponse)
async def update_note(
    order_id: UUID,
    note_id: UUID,
    note: OrderNoteUpdate,
    db: AsyncSession = Depends(get_db),
):
    return await update_note_to_order(
        db=db, order_id=order_id, note=note, note_id=note_id
    )


@router.delete("/{order_id}/notes/{note_id}")
async def delete_note(
    order_id: UUID,
    note_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    return await delete_note_to_order(db=db, order_id=order_id, note_id=note_id)
