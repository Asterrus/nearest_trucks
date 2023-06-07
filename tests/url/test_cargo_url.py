
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status

from database.crud.cargo import create
from database.models import Cargo
from tests.crud.conftest import location_valid_data_3, create_location, \
    location_valid_data_4


async def test_get_all_cargoes(client: AsyncClient, session: AsyncSession, test_data_cargo, test_data_truck):
    """
    Test that it is possible to get a list of all cargoes.
    """
    cargo_2_pick_up = await create_location(session, location_valid_data_3)
    cargo_2_delivery = await create_location(session, location_valid_data_4)
    await create(session, cargo_2_pick_up, cargo_2_delivery, 100, 'test_cargo_2')

    await session.commit()

    response: Response = await client.get(url='cargoes/all_cargoes')
    assert response.status_code == status.HTTP_200_OK, f"Expected status code {status.HTTP_200_OK}, but got {response.status_code}."
    assert len(response.json()) == 2, "Expected 2 cargoes in the response."
    assert response.json()[0]['nearest_trucks'] == 0, "Expected nearest_trucks to be 0 for the first cargo in the response."
    assert response.json()[1]['nearest_trucks'] == 1, "Expected nearest_trucks to be 1 for the second cargo in the response."


async def test_get_all_cargoes(client: AsyncClient, session: AsyncSession, test_data_cargo, test_data_truck):
    """
    Test that it is possible to get a list of all cargoes.
    """
    cargo_2_pick_up = await create_location(session, location_valid_data_3)
    cargo_2_delivery = await create_location(session, location_valid_data_4)
    await create(session, cargo_2_pick_up, cargo_2_delivery, 100, 'test_cargo_2')

    await session.commit()

    response: Response = await client.get(url='cargoes/all_cargoes')
    assert response.status_code == status.HTTP_200_OK, f"Expected status code {status.HTTP_200_OK}, but got {response.status_code}."
    assert len(response.json()) == 2, "Expected 2 cargoes in the response."
    assert response.json()[0]['nearest_trucks'] == 0, "Expected nearest_trucks to be 0 for the first cargo in the response."
    assert response.json()[1]['nearest_trucks'] == 1, "Expected nearest_trucks to be 1 for the second cargo in the response."


async def test_get_cargo(client: AsyncClient, session: AsyncSession, test_data_cargo: Cargo, test_data_truck):
    """
    Test that it is possible to get cargo information by its id.
    """
    response: Response = await client.get(url=f'cargoes/{100}')
    assert response.status_code == status.HTTP_404_NOT_FOUND, f"Expected status code {status.HTTP_404_NOT_FOUND}, but got {response.status_code}."
    assert response.content == b'{"detail":"Cargo model instance not found."}', "Expected 'detail' field to contain 'Cargo model instance not found.' in the response content."

    cargo, pick_up_location, delivery_location = test_data_cargo
    truck, truck_location = test_data_truck
    response: Response = await client.get(url=f'cargoes/{cargo.id}')
    assert response.status_code == status.HTTP_200_OK, f"Expected status code {status.HTTP_200_OK}, but got {response.status_code}."
    assert response.json()['pick_up_location'] == {'city': pick_up_location.city, 'state': pick_up_location.state, 'postcode': pick_up_location.postcode}, "Unexpected pick_up_location in the response."
    assert response.json()['delivery_location'] == {'city': delivery_location.city, 'state': delivery_location.state, 'postcode': delivery_location.postcode}, "Unexpected delivery_location in the response."
    assert response.json()['trucks'] == [{'VIN': truck.VIN, 'distance': 2239.76}], "Unexpected trucks list in the response."


async def test_edit_cargo(client: AsyncClient, session: AsyncSession, test_data_cargo: Cargo):
    """
    Test that it is possible to edit cargo information by its id.
    """
    cargo, pick_up_location, delivery_location = test_data_cargo
    assert cargo.description == 'test_cargo'
    assert cargo.weight == 100
    new_data = {
        'description': 'new_test_cargo',
        'weight': 200
    }
    response: Response = await client.patch(url=f'cargoes/{cargo.id}/edit', json=new_data)
    await session.refresh(cargo)
    assert response.status_code == status.HTTP_200_OK, f"Expected status code {status.HTTP_200_OK}, but got {response.status_code}."
    assert cargo.description == 'new_test_cargo', "Unexpected cargo description after update."
    assert cargo.weight == 200, "Unexpected cargo weight after update."
    assert response.json()['description'] == new_data['description'], "Unexpected description in the response."
    assert response.json()['weight'] == new_data['weight'], "Unexpected weight in the response."
    assert response.json()['id'] == cargo.id, "Unexpected id in the response."


async def test_add_cargo(client: AsyncClient, session: AsyncSession):
    """
    Test that it is possible to add a new cargo.
    """
    pick_up_location = await create_location(session, location_valid_data_3)
    delivery_location = await create_location(session, location_valid_data_4)
    await session.commit()

    data = {
        "zip_pick_up": pick_up_location.postcode,
        "zip_delivery": delivery_location.postcode,
        "weight": 100,
        "description": "test cargo"
    }
    response: Response = await client.post(url='cargoes/add', json=data)
    assert response.status_code == status.HTTP_201_CREATED, f"Expected status code {status.HTTP_201_CREATED}, but got {response.status_code}."
    assert response.json()['pick_up_location_id'] == pick_up_location.id, "Unexpected pick_up_location_id in the response."
    assert response.json()['delivery_location_id'] == delivery_location.id, "Unexpected delivery_location_id in the response."

    wrong_data = {
        "zip_pick_up": pick_up_location.postcode,
        "zip_delivery": pick_up_location.postcode,
        "weight": 100,
        "description": "test cargo"
    }
    response: Response = await client.post(url='cargoes/add', json=wrong_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, f"Expected status code {status.HTTP_422_UNPROCESSABLE_ENTITY}, but got {response.status_code}."
    assert response.json()['detail'][0]['msg'] == 'zip_pick_up and zip_delivery must be different', "Unexpected error message in the response."


async def test_delete_cargo(client: AsyncClient, session: AsyncSession, test_data_cargo):
    """
    Test that it is possible to delete a cargo by its id.
    """
    cargo, pick_up_location, delivery_location = test_data_cargo

    response: Response = await client.delete(url=f'cargoes/{cargo.id}/delete')
    assert response.status_code == status.HTTP_200_OK, f"Expected status code {status.HTTP_200_OK}, but got {response.status_code}."
    assert response.json()['message'] == f"Cargo with id:{cargo.id} deleted", "Unexpected message in the response."

    # Check if the cargo is actually deleted
    response = await client.get(url=f'cargoes/{cargo.id}')
    assert response.status_code == status.HTTP_404_NOT_FOUND, f"Expected status code {status.HTTP_404_NOT_FOUND}, but got {response.status_code}."
    assert response.content == b'{"detail":"Cargo model instance not found."}', "Expected 'detail' field to contain 'Cargo model instance not found.' in the response content."