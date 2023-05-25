from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Cargo, Location
from schemas import CargoCreate, CargoEdit


async def get(db: AsyncSession, id: int):
    return await db.get(Cargo, id)


async def find_loc_id_by_zip(db, zip: str):
    stmt = select(Location.id).filter(Location.postcode == zip)
    location = await db.execute(stmt)
    return location.scalar_one_or_none()


async def create(db: AsyncSession, pick_up_location_id: int,
                 delivery_location_id: int, weight: int, description: str):
    new_cargo = Cargo(
        pick_up_location_id=pick_up_location_id,
        delivery_location_id=delivery_location_id,
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
