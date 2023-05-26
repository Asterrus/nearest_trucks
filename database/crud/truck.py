from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Truck, Location


async def update(db: AsyncSession, location: Location, truck: Truck) -> Truck:
    truck.location_id = location.id
    await db.commit()
    return truck
