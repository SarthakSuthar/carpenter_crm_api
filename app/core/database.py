import urllib.parse

from pydantic_core import Url
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import urllib

from app.main import DATABASE_URL


engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,  # Use future=True for SQLAlchemy 2.0 style
)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
Base = declarative_base()
