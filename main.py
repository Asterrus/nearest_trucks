import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from database.db import async_session_maker
from routers.cargo import cargo_router
from routers.truck import truck_router
from utils.functions import (create_trucks, import_locations,
                             update_truck_locations)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_session_maker() as session:
        await import_locations(session)
    async with async_session_maker() as session:
        await create_trucks(session)
    async with async_session_maker() as session:
        asyncio.create_task(update_truck_locations(session))
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(cargo_router)
app.include_router(truck_router)
