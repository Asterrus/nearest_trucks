from pydantic import BaseModel, Field, validator

from schemas.location import LocationDisplay
from schemas.truck import TruckForCargo


class CargoBase(BaseModel):
    description: str
    weight: int = Field(ge=1, le=1000)


class CargoEdit(CargoBase):
    pass


class CargoInput(CargoBase):
    zip_pick_up: str
    zip_delivery: str

    @validator('zip_delivery')
    def validate_zip_codes(cls, v, values):
        if v == values['zip_pick_up']:
            raise ValueError('zip_pick_up and zip_delivery must be different')
        return v


class CargoCreate(CargoBase):
    pick_up_location_id: int
    delivery_location_id: int


class CargoDisplay(BaseModel):
    pick_up_location: LocationDisplay
    delivery_location: LocationDisplay


class CargoDisplaySingle(CargoDisplay):
    trucks: list[TruckForCargo]


class CargoDisplayMany(CargoDisplay):
    nearest_trucks: int


class Cargo(CargoBase):
    id: int
    pick_up_location_id: int
    delivery_location_id: int

    class Config:
        orm_mode = True
