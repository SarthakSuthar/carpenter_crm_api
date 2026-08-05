from contextlib import asynccontextmanager

from api.v1.api_router import auth_router, order_router, user_router
from core.config import get_settings
from core.database import engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(title=settings.app_name, lifespan=lifespan)

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(order_router)
app.include_router(user_router)


@app.get("/health")
def read_root():
    return {"status": "get_settings().database_url"}
