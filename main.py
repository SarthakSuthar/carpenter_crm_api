from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.api_router import auth_router, order_router, user_router
from app.core.config import get_settings
from app.core.database import engine

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.include_router(auth_router)
app.include_router(order_router)
app.include_router(user_router)


@app.get("/health")
def read_root():
    return {"status": get_settings().database_url}
