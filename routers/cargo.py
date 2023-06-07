from fastapi import status
from fastapi.concurrency import run_in_threadpool
from fastapi.routing import APIRouter

from database.crud.base import get_all_objects, get_object_or_404
from database.crud.cargo import create, delete, update
from database.db import database
from database.models import Cargo as CargoModel
from database.models import Location
from database.models import Truck as TruckModel
from schemas.cargo import (Cargo, CargoDisplayMany, CargoDisplaySingle,
                           CargoEdit, CargoInput)
from schemas.truck import TruckForCargo
from utils.functions import find_distance

cargo_router = APIRouter(
    tags=['cargo'],
    prefix='/cargoes',
)


@cargo_router.get('/all_cargoes', response_model=list[CargoDisplayMany])
async def get_all_cargoes(db: database, max_distance: int | None = 450,
                          max_weight: int | None = None):
    """Getting a list of all cargoes as well as the number of trucks
     within a certain distance from them.
      Filters are available for maximum
     weight, and distance between the load and the truck."""
    cargoes = await get_all_objects(db, CargoModel)
    trucks = await get_all_objects(db, TruckModel)
    cargoes_list = []
    for cargo in cargoes:
        if max_weight and cargo.weight > max_weight:
            continue
        nearest_tracks = 0
        for truck in trucks:
            distance = await run_in_threadpool(
                find_distance, cargo.pick_up_location, truck.location)
            if distance <= max_distance:
                nearest_tracks += 1

        cargoes_list.append(CargoDisplayMany(
            pick_up_location=cargo.pick_up_location,
            delivery_location=cargo.delivery_location,
            nearest_trucks=nearest_tracks))
    return cargoes_list


@cargo_router.get('/{id}', response_model=CargoDisplaySingle)
async def get_cargo(db: database, id: int):
    """Finds an instance of the Cargo model by its id and returns information
     about it, as well as a list of distances from each truck to that cargo"""
    cargo = await get_object_or_404(db, CargoModel, CargoModel.id == id)
    trucks = await get_all_objects(db, TruckModel)
    trucks_list = []
    for truck in trucks:
        distance = await run_in_threadpool(
            find_distance, cargo.pick_up_location, truck.location)
        trucks_list.append(TruckForCargo(
            VIN=truck.VIN, distance=round(distance, 2)))
    trucks_list.sort(key=lambda x: x.distance)
    return CargoDisplaySingle(pick_up_location=cargo.pick_up_location,
                              delivery_location=cargo.delivery_location,
                              trucks=trucks_list)


@cargo_router.post('/add', response_model=Cargo,
                   status_code=status.HTTP_201_CREATED)
async def add_cargo(db: database, cargo: CargoInput):
    """Adding an instance of cargo. Valid zip codes are required."""
    pick_up_location = await get_object_or_404(
        db, Location, Location.postcode == cargo.zip_pick_up, 'zip_pick_up')
    delivery_location = await get_object_or_404(
        db, Location, Location.postcode == cargo.zip_delivery, 'zip_delivery')
    return await create(db, pick_up_location, delivery_location,
                        cargo.weight, cargo.description)


@cargo_router.patch('/{id}/edit', response_model=Cargo)
async def edit_cargo(db: database, cargo_data: CargoEdit, id: int):
    """Changing the cargo instance by id"""
    cargo = await get_object_or_404(db, CargoModel, CargoModel.id == id)
    await update(db, cargo_data, cargo)
    return cargo


@cargo_router.delete('/{id}/delete')
async def delete_cargo(db: database, id: int):
    """Deleting a cargo instance by id"""
    cargo = await get_object_or_404(db, CargoModel, CargoModel.id == id)
    await delete(db, cargo)
    return {"message": f"Cargo with id:{id} deleted"}
