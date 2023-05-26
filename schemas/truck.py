from pydantic import BaseModel, Field, validator

from utils.validators import vin_validator


class TruckBase(BaseModel):
    capacity: int = Field(ge=1, le=1000)
    VIN: str

    @validator('VIN')
    def validate_vin(cls, v, values):
        return vin_validator(v)


class TruckEdit(BaseModel):
    zip: str


class TruckForCargo(BaseModel):
    VIN: str
    distance: float


class Truck(TruckBase):
    id: int
    location_id: int

    class Config:
        orm_mode = True
