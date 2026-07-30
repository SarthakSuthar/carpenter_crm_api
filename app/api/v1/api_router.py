from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])

order_router = APIRouter(prefix="/order", tags=["order"])

user_router = APIRouter(prefix="/user", tags=["user"])
