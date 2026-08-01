from app.api.v1.auth import router as auth_router
from app.api.v1.order import router as order_router
from app.api.v1.user import router as user_router

__all__ = ["auth_router", "order_router", "user_router"]
