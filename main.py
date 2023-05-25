from contextlib import asynccontextmanager

from fastapi import FastAPI

from routers.cargo import cargo_router
from utils.functions import import_locations, create_trucks
from database.db import async_session_maker


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_session_maker() as session:
        await import_locations(session)
    async with async_session_maker() as session:
        await create_trucks(session)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(cargo_router)


@app.get('/')
async def hello():
    return {'text': 'hello!'}
