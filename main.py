from contextlib import asynccontextmanager

from fastapi import FastAPI

from data.import_locations import import_locations
from database.db import database, get_async_session, async_session_maker


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_session_maker() as session:
        await import_locations(session)
    yield

app = FastAPI(lifespan=lifespan)



@app.get('/')
async def hello():
    return {'text': 'hello!'}
