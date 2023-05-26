from fastapi.routing import APIRouter

from database.crud.base import get_object_or_404
from database.crud.truck import update
from database.db import database
from database.models import Location
from database.models import Truck as TruckModel
from schemas.truck import Truck, TruckEdit

truck_router = APIRouter(
    tags=['truck'],
    prefix='/trucks'
)


@truck_router.patch('/{id}/edit', response_model=Truck)
async def edit_truck(db: database, truck_data: TruckEdit, id: int):
    truck = await get_object_or_404(db, TruckModel, TruckModel.id == id)
    location = await get_object_or_404(db, Location,
                                       Location.postcode == truck_data.zip)
    await update(db, location, truck)
    return truck
