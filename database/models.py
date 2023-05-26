from sqlalchemy import CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.orm import (Mapped, mapped_column, DeclarativeBase,
                            declared_attr, relationship, validates)

from config import CARGO_MIN_WEIGHT, CARGO_MAX_WEIGHT, TRUCK_MIN_CAPACITY, \
    TRUCK_MAX_CAPACITY
from utils.validators import vin_validator


class Base(DeclarativeBase):

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True, index=True)


class Location(Base):
    city: Mapped[str]
    state: Mapped[str]
    postcode: Mapped[str]
    latitude: Mapped[float]
    longitude: Mapped[float]

    __table_args__ = (
        CheckConstraint('latitude >= -90', 'min_latitude_-90_constraint'),
        CheckConstraint('latitude <= 90', 'max_latitude_90_constraint'),
        CheckConstraint('longitude >= -180', 'min_longitude_-180_constraint'),
        CheckConstraint('longitude <= 180', 'max_longitude_180_constraint'),
        UniqueConstraint('latitude', 'longitude',
                         name='unique_latitude_longitude_constraint'),
    )

    def __repr__(self) -> str:
        return (f"Location(id={self.id!r},"
                f" latitude={self.latitude!r}, longitude={self.longitude!r})")


class Truck(Base):
    capacity: Mapped[int]
    location: Mapped["Location"] = relationship(lazy="selectin")
    location_id: Mapped[int] = mapped_column(
        ForeignKey('location.id'), index=True)
    VIN: Mapped[str] = mapped_column(unique=True)

    __table_args__ = (
        CheckConstraint(f'capacity >= {TRUCK_MIN_CAPACITY}',
                        f'min_capacity_{TRUCK_MIN_CAPACITY}_constraint'),
        CheckConstraint(f'capacity <= {TRUCK_MAX_CAPACITY}',
                        f'max_capacity_{TRUCK_MAX_CAPACITY}_constraint'),
    )

    @validates('VIN')
    def validate_vin(self, key, value):
        return vin_validator(value)

    def __repr__(self) -> str:
        return f"Truck(id={self.id!r}, VIN={self.VIN!r})"


class Cargo(Base):
    weight: Mapped[int]
    description: Mapped[str]
    pick_up_location_id: Mapped[int] = mapped_column(
        ForeignKey('location.id'), index=True)
    delivery_location_id: Mapped[int] = mapped_column(
        ForeignKey('location.id'), index=True)
    pick_up_location: Mapped["Location"] = relationship(
        foreign_keys=[pick_up_location_id], lazy="selectin")
    delivery_location: Mapped["Location"] = relationship(
        foreign_keys=[delivery_location_id], lazy="selectin")

    __table_args__ = (
        CheckConstraint(f'weight >= {CARGO_MIN_WEIGHT}',
                        f'min_weight_{CARGO_MIN_WEIGHT}_constraint'),
        CheckConstraint(f'weight <= {CARGO_MAX_WEIGHT}',
                        f'max_weight_{CARGO_MAX_WEIGHT}_constraint'),
        CheckConstraint('pick_up_location_id != delivery_location_id',
                        'different_locations_constraint'),
    )

    def __repr__(self) -> str:
        return f"Cargo(id={self.id!r}, description={self.description[:20]!r})"
