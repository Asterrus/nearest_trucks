import os
import csv

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Location
from config import DATA_FOLDER


async def import_locations(session: AsyncSession):
    with open(os.path.join(DATA_FOLDER, 'uszips.csv'), "r") as file:
        csv_file = csv.DictReader(file,
                                  fieldnames=['zip', 'lat', 'lng', 'city',
                                              'state_name'])
        headers = next(csv_file)
        locations = [Location(postcode=int(row['zip']), city=row['city'],
                              longitude=float(row['lng']), state=row['state_name'],
            latitude=float(row['lat']),
        ) for row in csv_file]
        session.add_all(locations)
    try:
        await session.commit()
    except IntegrityError:
        print('Locations already imported')
    except Exception as e:
        print(e)
