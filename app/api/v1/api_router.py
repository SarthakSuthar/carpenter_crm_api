from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])

order_router = APIRouter(prefix="/orders", tags=["order"])

user_router = APIRouter(prefix="/user", tags=["user"])
