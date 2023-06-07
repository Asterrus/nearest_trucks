import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from database.db import get_async_session
from database.models import Base
from config import (DB_HOST_TEST, DB_NAME_TEST, DB_PASS_TEST, DB_PORT_TEST,
                    DB_USER_TEST)
from main import app

DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
metadata = Base.metadata
metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Async fixture that overrides the get_async_session dependency in the FastAPI app to use the test database session.
    """
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    """
    Fixture that creates all tables in the test database before all tests run and drops them after all tests.
    """
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(autouse=True)
async def cleanup_database(session: AsyncSession):
    """
    Fixture that cleans up the database after each test by deleting all records from all tables.
    """
    async with session.begin():
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())


@pytest.fixture(scope='session')
def event_loop(request):
    """
    Fixture that creates an instance of the default event loop for each test case.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that provides an AsyncClient instance that can be used in tests to make HTTP requests to the FastAPI app.
    """
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as client:
        yield client


@pytest.fixture(scope='function')
async def session() -> AsyncGenerator[AsyncSession, None]:
    """
    Fixture that provides an AsyncSession instance for the test database.
    """
    async with async_session_maker() as session:
        yield session