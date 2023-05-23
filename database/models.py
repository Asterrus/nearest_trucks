from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Truck(Base):
    __tablename__ = 'truck'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    capacity: Mapped[int]