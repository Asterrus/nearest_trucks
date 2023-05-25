from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Location
from utils.exceptions import InvalidZip


async def valid_zip(db: AsyncSession, zip: str):
    print('valid_zip')
    location = await get_loc_by_zip(db, zip)
    if location is None:
        raise InvalidZip(zip)
    return location


async def get_loc_by_zip(db: AsyncSession, zip: str):
    stmt = select(Location.id).where(Location.postcode == zip)
    location = await db.execute(stmt)
    print(location)
    return location.scalar_one_or_none()