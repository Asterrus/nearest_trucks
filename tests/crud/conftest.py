import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Location, Truck

location_valid_data_1 = {'city': 'test_city_1','state': 'test_state_1',
                         'postcode': '123', 'latitude': 23, 'longitude': 123}

location_valid_data_2 = {'city': 'test_city_2', 'state': 'test_state_2',
                         'postcode': '124', 'latitude': 76, 'longitude': 156}

location_valid_data_3 = {'city': 'test_city_3', 'state': 'test_state_3',
                         'postcode': '125', 'latitude': 51, 'longitude': 101}

location_valid_data_4 = {'city': 'test_city_4', 'state': 'test_state_4',
                         'postcode': '126', 'latitude': 54, 'longitude': 105}

@pytest.fixture
async def create_two_locations(session: AsyncSession):
    first_location = Location(**location_valid_data_1)
    second_location = Location(**location_valid_data_2)
    session.add_all([first_location, second_location])
    locations = await session.scalars(select(Location))
    assert len(locations.all()) == 2, 'locations not created'
    return first_location, second_location


async def create_location(session: AsyncSession, location_data=None):
    if location_data:
        location = Location(**location_data)
    else:
        location = Location(**location_valid_data_1)
    session.add(location)
    query = select(Location).where(Location.latitude == location.latitude,
                                   Location.longitude == location.longitude)
    location = await session.scalar(query)
    return location


async def create_truck(session: AsyncSession, truck_data=None):
    if truck_data:
        location = Truck(**truck_data)
    else:
        location = Location(**location_valid_data_1)
    session.add(location)
    query = select(Location).where(Location.latitude == location.latitude,
                                   Location.longitude == location.longitude)
    location = await session.scalar(query)
    return location