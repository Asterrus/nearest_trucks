from sqlalchemy import CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.orm import (Mapped, mapped_column, DeclarativeBase,
                            declared_attr, relationship, validates)


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
        return (f"Truck(id={self.id!r},"
                f" latitude={self.latitude!r}, longitude={self.longitude!r})")


class Truck(Base):
    capacity: Mapped[int]
    location: Mapped["Location"] = relationship()
    location_id: Mapped[int] = mapped_column(ForeignKey('location.id'))
    VIN: Mapped[str] = mapped_column(unique=True)

    __table_args__ = (
        CheckConstraint('capacity >= 1', 'min_capacity_1_constraint'),
        CheckConstraint('capacity <= 1000', 'max_capacity_1000_constraint'),
    )

    @validates('VIN')
    def validate_vin(self, key, value):
        if len(value) != 5:
            raise ValueError('The VIN length should be 5')
        if not 1000 <= int(value[:4]) <= 9999:
            raise ValueError('The VIN number should be between 1000 and 9999')
        if not 'A' <= value[-1] <= 'Z':
            raise ValueError('The letter must be a capital English letter')
        return value

    def __repr__(self) -> str:
        return f"Truck(id={self.id!r}, VIN={self.VIN!r})"


class Cargo(Base):
    weight: Mapped[int] = mapped_column(CheckConstraint('1 <= weight <= 1000'))
    description: Mapped[str]
    pick_up_location_id: Mapped[int] = mapped_column(ForeignKey('location.id'))
    delivery_location_id: Mapped[int] = mapped_column(
        ForeignKey('location.id'))
    pick_up_location: Mapped["Location"] = relationship(
        foreign_keys=[pick_up_location_id])
    delivery_location: Mapped["Location"] = relationship(
        foreign_keys=[delivery_location_id])

    __table_args__ = (
        CheckConstraint('weight >= 1', 'min_weight_1_constraint'),
        CheckConstraint('weight <= 1000', 'max_weight_1000_constraint'),
        CheckConstraint('pick_up_location_id != delivery_location_id',
                        'different_locations_constraint'),
    )

    def __repr__(self) -> str:
        return f"Cargo(id={self.id!r}, description={self.description[:20]!r})"
