import pandas as pd
from sqlalchemy import create_engine, types
from sqlalchemy.types import String, Integer, Date, TIMESTAMP, Float

data = pd.read_csv('ks-projects/ks-projects-201801.csv')

map_columns_to_types = {
    "ID": Integer,
    "name": String,
    "category": String,
    "main_category": String,
    "currency": String,
    "deadline": Date,
    "goal": Float,
    "launched": TIMESTAMP,
    "pledged": Float,
    "state": String,
    "backers": Integer,
    "country": String,
    "usd pledged": Float,
    "usd_pledged_real": Float,
    "usd_goal_real": Float
}

engine = create_engine('mysql://sk-user:secret@db:3306/sk')

data.to_sql(
    "projects", # Nombre de la tabla
    con=engine, # Conexión a la base de datos
    dtype=map_columns_to_types) # Mapeo de las columnas del archivo csv a los tipos de mysql
