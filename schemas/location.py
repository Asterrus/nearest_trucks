from pydantic import BaseModel


class LocationBase(BaseModel):
    city: str
    state: str
    postcode: str


class LocationDisplay(LocationBase):
    class Config:
        orm_mode = True
