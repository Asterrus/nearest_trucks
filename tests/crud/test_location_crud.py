from copy import copy

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Location
from tests.crud.conftest import create_location

MODEL = Location


async def test_add_location_valid_data(session: AsyncSession):
    """
    Test that a valid Location object is created successfully
    """
    location = await create_location(session)
    assert location is not None, f'{MODEL.__name__} object was not created'


async def test_add_location_invalid_data(session: AsyncSession):
    """
    Test that an invalid Location object is not created and raises IntegrityError
    """
    wrong_data = {'city': 'test_city_2', 'state': 'test_state_2',
                  'postcode': '124', 'latitude': 200, 'longitude': 400}

    with pytest.raises(IntegrityError):
        await create_location(session, location_data=wrong_data)


async def test_add_location_duplicate(session: AsyncSession):
    """
    Test that a duplicate Location object is not created and raises IntegrityError
    """
    location = await create_location(session)
    assert location is not None, f'{MODEL.__name__} object was not created'

    with pytest.raises(IntegrityError):
        await create_location(session)


async def test_delete_location(session: AsyncSession):
    """
    Test that a Location object is deleted successfully
    """
    location = await create_location(session)
    assert location is not None, f'{MODEL.__name__} object was not created'

    await session.delete(location)
    location = await session.scalar(select(Location))

    assert not location, f'{MODEL.__name__} object not deleted'
