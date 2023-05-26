from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Truck


async def update(db: AsyncSession, location_id: int, truck: Truck) -> Truck:
    truck.location_id = location_id
    await db.commit()
    return truck
