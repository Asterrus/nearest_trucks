from fastapi.routing import APIRouter
from fastapi import Response, HTTPException, status
from fastapi.responses import Response
from database.crud.cargo import create, get, update, delete
from database.db import database
from schemas import Cargo, CargoInput, CargoEdit
from utils.dependencies import valid_zip
from utils.exceptions import InvalidZip

cargo_router = APIRouter(
    tags=['cargo'],
    prefix='/cargoes'
)


@cargo_router.post('/add', response_model=Cargo)
async def add_cargo(db: database, cargo: CargoInput):
    try:
        pick_up_location_id = await valid_zip(db, cargo.zip_pick_up)
        delivery_location_id = await valid_zip(db, cargo.zip_delivery)
    except InvalidZip as err:
        raise HTTPException(
            detail=err.text, status_code=status.HTTP_404_NOT_FOUND)
    return await create(db, pick_up_location_id, delivery_location_id,
                        cargo.weight, cargo.description)


@cargo_router.patch('/{id}/edit', response_model=Cargo)
async def edit_cargo(db: database, cargo_data: CargoEdit, id: int):
    cargo = await get(db, id)
    if cargo is None:
        raise HTTPException(
            detail='cargo not found', status_code=status.HTTP_404_NOT_FOUND)
    await update(db, cargo_data, cargo)
    return cargo


@cargo_router.delete('/{id}/delete')
async def delete_cargo(db: database, id: int):
    cargo = await get(db, id)
    if cargo is None:
        raise HTTPException(
            detail='cargo not found', status_code=status.HTTP_404_NOT_FOUND)
    await delete(db, cargo)
    return {"message": f"Cargo with id:{id} deleted"}