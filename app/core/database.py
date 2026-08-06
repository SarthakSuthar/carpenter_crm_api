from core.config import get_settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

settings = get_settings()

DATABASE_URL = settings.database_url


engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    poolclass=NullPool,
    connect_args={"statement_cache_size": 0},
)

async_session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)
