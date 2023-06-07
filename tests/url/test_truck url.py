from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status

from database.models import Location
from tests.crud.conftest import create_location, location_valid_data_2


async def test_edit_truck_valid_data(client: AsyncClient, session: AsyncSession, test_data_truck):
    """
    Test that it is possible to successfully edit truck information.
    """
    another_location: Location = await create_location(session, location_valid_data_2)
    await session.commit()

    truck, location = test_data_truck
    data = {
        "zip": another_location.postcode
    }
    response: Response = await client.patch(url=f'trucks/{truck.id}/edit', json=data)
    assert response.status_code == status.HTTP_200_OK, f"Expected status code {status.HTTP_200_OK}, but got {response.status_code}."
    assert response.json() == {'capacity': truck.capacity, 'VIN': '1234Z', 'id': truck.id, 'location_id': another_location.id}, "Unexpected response JSON."
    await session.refresh(truck)
    assert truck.location is another_location, "Truck location was not updated as expected."


async def test_edit_truck_invalid_data(client: AsyncClient, session: AsyncSession, test_data_truck):
    """
    Test that it is not possible to edit truck information with invalid data.
    """
    truck, location = test_data_truck
    data = {
        "zip": '999'
    }
    response: Response = await client.patch(url=f'trucks/{truck.id}/edit', json=data)
    assert response.status_code == status.HTTP_404_NOT_FOUND, f"Expected status code {status.HTTP_404_NOT_FOUND}, but got {response.status_code}."
    assert response.is_error, "Response should be an error."
    assert truck.location is location, "Truck location should not have been updated."
    assert response.content == b'{"detail":"Location model instance not found.Invalid input data: (\'zip\',)"}', "Unexpected response content."


async def test_edit_truck_wrong_truck(client: AsyncClient, session: AsyncSession):
    """
    Test that it is not possible to edit information for a non-existent truck.
    """
    data = {
        "zip": '999'
    }
    response: Response = await client.patch(url=f'trucks/{777}/edit', json=data)
    assert response.status_code == status.HTTP_404_NOT_FOUND, f"Expected status code {status.HTTP_404_NOT_FOUND}, but got {response.status_code}."
    assert response.is_error, "Response should be an error."
    assert response.content == b'{"detail":"Truck model instance not found."}', "Unexpected response content."