import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud.cargo import create
from database.models import Truck, Cargo
from tests.crud.conftest import create_location, location_valid_data_2, \
    create_two_locations


@pytest.fixture
async def test_data_truck(session: AsyncSession):
    truck_location = {
        'city': 'test_city_3',
        'state': 'test_state_3',
        'postcode': '125',
        'latitude': 50,
        'longitude': 100
    }
    location = await create_location(session, truck_location)
    truck = Truck(capacity=100, location_id=location.id, VIN='1234Z')
    session.add(truck)
    await session.commit()
    return truck, location


@pytest.fixture
async def test_data_cargo(session: AsyncSession, create_two_locations):
    pick_up_location, delivery_location = create_two_locations
    cargo = Cargo(weight=100, description='test_cargo',
                  pick_up_location=pick_up_location, delivery_location=delivery_location)
    session.add(cargo)
    await session.commit()
    return cargo, pick_up_location, delivery_location
