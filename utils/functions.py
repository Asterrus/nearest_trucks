import os
import csv
import random

from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Location, Truck
from config import DATA_FOLDER


async def import_locations(session: AsyncSession):
    with open(os.path.join(DATA_FOLDER, 'uszips.csv'), "r") as file:
        csv_file = csv.DictReader(file,
                                  fieldnames=['zip', 'lat', 'lng', 'city',
                                              'state_name'])
        headers = next(csv_file)
        locations = [Location(
            postcode=row['zip'],
            city=row['city'],
            longitude=float(row['lng']),
            state=row['state_name'],
            latitude=float(row['lat']),
        ) for row in csv_file]
        session.add_all(locations)
    try:
        await session.commit()
    except IntegrityError:
        print('Locations already imported')
    except Exception as e:
        print(e)


async def create_trucks(session: AsyncSession):
    stmt = select(Location.id).order_by(func.random()).limit(20)
    location_ids = await session.execute(stmt)
    location_ids_list = location_ids.scalars().all()
    trucks = [Truck(
        capacity=random.randint(1, 1000),
        location_id=location_ids_list[i],
        VIN=str(1000+i)+'A'
    ) for i in range(20)]
    session.add_all(trucks)
    try:
        await session.commit()
    except IntegrityError:
        print('Trucks already created')
    except Exception as e:
        print(e)
