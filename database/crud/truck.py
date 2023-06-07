from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Location, Truck


async def update(db: AsyncSession, location: Location, truck: Truck) -> Truck:
    truck.location = location
    await db.commit()
    await db.refresh(truck)
    return truck
