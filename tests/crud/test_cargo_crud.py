import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud.cargo import create, delete, update
from database.models import Cargo
from schemas.cargo import CargoEdit

MODEL = Cargo


async def test_add_cargo_valid_data(session: AsyncSession, create_two_locations):
    """
    Test that a valid Cargo object is created successfully
    """
    first_locations, second_locations = create_two_locations
    cargo = await create(session, first_locations, second_locations, 100, 'test_description')
    assert cargo, f'{MODEL.__name__} object not created'


async def test_add_cargo_invalid_data(session: AsyncSession, create_two_locations):
    """
    Test that an invalid Cargo object is not created and raises IntegrityError
    """
    first_locations, second_locations = create_two_locations
    with pytest.raises(IntegrityError):
        await create(session, first_locations, second_locations, 1001, 'test_description')


async def test_update_cargo_valid_data(session: AsyncSession, create_two_locations):
    """
    Test that a Cargo object is updated successfully with valid data
    """
    first_locations, second_locations = create_two_locations
    cargo = await create(session, first_locations, second_locations, 100, 'test_description')
    assert cargo, f'{MODEL.__name__} object not created'
    cargo_data = CargoEdit(description='test_description_2', weight=101)
    await update(session, cargo_data, cargo)
    assert cargo.weight == 101, f'{MODEL.__name__} object not updated correctly'
    assert cargo.description == 'test_description_2', f'{MODEL.__name__} object not updated correctly'


async def test_delete_cargo(session: AsyncSession, create_two_locations):
    """
    Test that a Cargo object is deleted successfully
    """
    first_locations, second_locations = create_two_locations
    cargo = await create(session, first_locations, second_locations, 100, 'test_description')
    assert cargo, f'{MODEL.__name__} object not created'
    await delete(session, cargo)
    cargo = await session.scalar(select(Cargo))
    assert not cargo, f'{MODEL.__name__} object not deleted'