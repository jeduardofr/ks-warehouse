# Desarrollado por:
# - Fuentes Rangel, Jesús Eduardo
# - López Barajas, Andrés Esaú
import pandas as pd
from sqlalchemy import create_engine, types
from sqlalchemy.types import String, Integer, Date, DATETIME, Float
from decouple import config

DB_NAME = config('DB_NAME')
DB_USERNAME = config('DB_USERNAME')
DB_PASSWORD = config('DB_PASSWORD')
DB_PORT = config('DB_PORT')
DB_HOST = config('DB_HOST')
DB_DRIVER = config('DB_DRIVER')

database_connection = "{}://{}:{}@{}:{}/{}?charset=utf8".format(DB_DRIVER, DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

def truncate_and_import_csv(file_path: str):
    data = pd.read_csv(file_path)

    map_columns_to_types = {
        "ID": Integer,
        "name": String(200),
        "category": String(200),
        "main_category": String(200),
        "currency": String(200),
        "deadline": Date,
        "goal": Float,
        "launched": DATETIME,
        "pledged": Float,
        "state": String(200),
        "backers": Integer,
        "country": String(200),
        "usd pledged": Float,
        "usd_pledged_real": Float,
        "usd_goal_real": Float
    }

    engine = create_engine(database_connection)

    engine.execute("drop table if exists projects")

    data.to_sql(
        "projects", # Nombre de la tabla
        con=engine, # Conexión a la base de datos
        dtype=map_columns_to_types) # Mapeo de las columnas del archivo csv a los tipos de mysql
