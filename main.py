import pandas as pd
from sqlalchemy import create_engine, types
from sqlalchemy.types import String, Integer, Date, DATETIME, Float

data = pd.read_csv('ks-projects/ks-projects-201801.csv')

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

engine = create_engine('mysql://root:@localhost:3306/ks')

engine.execute("drop table projects")

data.to_sql(
    "projects", # Nombre de la tabla
    con=engine, # Conexión a la base de datos
    dtype=map_columns_to_types) # Mapeo de las columnas del archivo csv a los tipos de mysql
