from dotenv import load_dotenv
import os
load_dotenv()

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('POSTGRES_DB')
DB_USER = os.environ.get('POSTGRES_USER')
DB_PASS = os.environ.get('POSTGRES_PASSWORD')

DATA_FOLDER = 'data/'
TRUCK_LOCATION_CHANGE_INTERVAL = 180
TRUCK_INIT_AMOUNT = 20
TRUCK_MIN_CAPACITY = 1
TRUCK_MAX_CAPACITY = 1000
VIN_MIN_NUMBER = 1000
CARGO_MIN_WEIGHT = 1
CARGO_MAX_WEIGHT = 1000