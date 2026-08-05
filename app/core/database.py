from core.config import get_settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

settings = get_settings()

DATABASE_URL = settings.database_url

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=5,
    max_overflow=10,
)

async_session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)
