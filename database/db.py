from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = (f"postgresql+asyncpg://{DB_USER}:{DB_PASS}"
                f"@{DB_HOST}:{DB_PORT}/{DB_NAME}")
engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession)


async def get_async_session() -> AsyncGenerator:
    async with async_session_maker() as session:
        yield session

database = Annotated[AsyncSession, Depends(get_async_session)]
