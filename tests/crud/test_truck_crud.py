from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud.truck import update
from database.models import Truck
from tests.crud.conftest import create_location, location_valid_data_2

MODEL = Truck


async def test_update_truck_valid_data(session: AsyncSession):
    """
    Test that a valid Truck object is updated successfully
    """

    location = await create_location(session)
    truck = Truck(capacity=100, location_id=location.id, VIN='1234Z')
    session.add(truck)
    truck: Truck | None = await session.scalar(select(Truck))
    assert truck, f'{MODEL.__name__} object not created'

    another_location = await create_location(session, location_valid_data_2)
    assert truck.location is location

    truck = await update(session, another_location, truck)
    assert truck.location == another_location
