import asyncpg
from core.config import settings
from contextlib import asynccontextmanager
from typing import AsyncGenerator

_db_pool: asyncpg.Pool | None = None


async def init_db_pool():
    global _db_pool
    _db_pool = await asyncpg.create_pool(
        user=settings.POSTGRES_USERNAME,
        password=settings.POSTGRES_PASSWORD,
        database=settings.POSTGRES_DB,
        host=settings.POSTGRES_SERVER,
        port=settings.POSTGRES_PORT,
        min_size=1,
        max_size=10,
    )


@asynccontextmanager
async def get_db() -> AsyncGenerator[asyncpg.Connection, None]:
    if _db_pool is None:
        raise RuntimeError(
            "Database pool is not initialized. Call init_db_pool() first."
        )
    async with _db_pool.acquire() as connection:
        yield connection
