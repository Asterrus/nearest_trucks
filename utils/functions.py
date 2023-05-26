import asyncio
import os
import csv
import random

from geopy import distance
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud.base import get_all_objects
from database.models import Location, Truck
from config import DATA_FOLDER, TRUCK_LOCATION_CHANGE_INTERVAL, \
    TRUCK_INIT_AMOUNT, TRUCK_MAX_CAPACITY, TRUCK_MIN_CAPACITY, VIN_MIN_NUMBER


async def import_locations(session: AsyncSession) -> None:
    """Imports locations to the database from a csv file."""
    with open(os.path.join(DATA_FOLDER, 'uszips.csv'), "r") as file:
        csv_file = csv.DictReader(file, fieldnames=['zip', 'lat', 'lng',
                                                    'city', 'state_name'])
        _ = next(csv_file)
        locations = [Location(postcode=row['zip'], state=row['state_name'],
                              longitude=float(row['lng']), city=row['city'],
                              latitude=float(row['lat'])) for row in csv_file]
        session.add_all(locations)
    try:
        await session.commit()
        print('Locations successfully imported')
    except IntegrityError:
        print('Locations already imported')
    except Exception as e:
        print(e)


async def create_trucks(session: AsyncSession) -> None:
    """Adds 20 trucks with random locations to the database"""
    stmt = select(Location.id).order_by(func.random()).limit(20)
    location_ids = await session.execute(stmt)
    location_ids_list = location_ids.scalars().all()

    trucks = [Truck(
        capacity=random.randint(TRUCK_MIN_CAPACITY, TRUCK_MAX_CAPACITY),
        VIN=str(VIN_MIN_NUMBER + i) + 'A',
        location_id=location_ids_list[i]
    ) for i in range(TRUCK_INIT_AMOUNT)]
    session.add_all(trucks)

    try:
        await session.commit()
        print('Trucks successfully created')
    except IntegrityError:
        print('Trucks already created')
    except Exception as e:
        print(e)


def find_distance(location1: Location, location2: Location) -> float:
    """Finds the distance between two locations using
     latitude and longitude with Geopy distance"""
    location1_coords = (location1.latitude, location1.longitude)
    location2_coords = (location2.latitude, location2.longitude)
    return distance.distance(location1_coords, location2_coords).miles


async def update_truck_locations(db: AsyncSession) -> None:
    """At a certain interval updates the location of all trucks"""
    while True:
        trucks = await get_all_objects(db, Truck)
        trucks_count = len(trucks)
        stmt = select(Location.id).order_by(func.random()).limit(trucks_count)
        location_ids = await db.scalars(stmt)
        location_ids_list = location_ids.all()
        for i in range(trucks_count):
            trucks[i].location_id = location_ids_list[i]
        await db.commit()
        await asyncio.sleep(TRUCK_LOCATION_CHANGE_INTERVAL)
