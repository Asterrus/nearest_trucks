from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Cargo, Location
from schemas.cargo import CargoEdit


async def create(db: AsyncSession, pick_up_location: Location,
                 delivery_location: Location,
                 weight: int, description: str) -> Cargo:
    new_cargo = Cargo(
        pick_up_location_id=pick_up_location.id,
        delivery_location_id=delivery_location.id,
        weight=weight, description=description)

    db.add(new_cargo)
    await db.commit()
    return new_cargo


async def update(db: AsyncSession, data: CargoEdit, cargo: Cargo):
    cargo.weight = data.weight
    cargo.description = data.description
    await db.commit()
    return cargo


async def delete(db: AsyncSession, cargo: Cargo):
    await db.delete(cargo)
    await db.commit()
