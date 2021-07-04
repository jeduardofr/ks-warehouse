import functools
import pandas as pd
from sqlalchemy.types import String, Integer, Date, DATETIME, Float
from pymongo import MongoClient, collection, mongo_client
from decouple import config

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask import jsonify
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from database import get_db
from auth import login_required

bp = Blueprint("project", __name__, url_prefix="/project")

@bp.route("/", methods=["GET"])
@login_required
def index():
    rows = get_db().execute("select * from projects limit 1000")
    return render_template('views/session/show-table.html', rows=rows)

@bp.route("/import", methods=["POST"])
@login_required
def import_projects():
    data = pd.read_csv(request.files['file'])

    map_columns_to_types = {
        "ID": Integer,
        "name": String(200),
        "category": String(200),
        "main_category": String(200),
        "currency": String(200),
        "deadline": Date,
        "launched": DATETIME,
        "goal": Float,
        "pledged": Float,
        "backers": Integer,
        "state": String(200),
        "country": String(200),
        "usd pledged": Float,
        "usd_pledged_real": Float,
        "usd_goal_real": Float
    }

    callback = lambda x: str(x).upper()

    data['name'] = data['name'].apply(callback)
    data['category'] = data['category'].apply(callback)
    data['main_category'] = data['main_category'].apply(callback)
    data['state'] = data['state'].apply(callback)
    data['country'] = data['country'].apply(callback)

    mongo_client = MongoClient("mongodb://{}:{}@{}:{}".format(
        config('MONGO_DB_USERNAME'),
        config('MONGO_DB_PASSWORD'),
        config('MONGO_DB_HOST'),
        config('MONGO_DB_PORT')
        ))
    mongo_db = mongo_client['kick-starter']
    project_collection = mongo_db['projects']
    project_collection.insert_many(data.to_dict('records'))

    db = get_db()
    db.execute("drop table if exists projects")
    data.to_sql(
        "projects", # Nombre de la tabla
        con=db, # Conexión a la base de datos
        dtype=map_columns_to_types) # Mapeo de las columnas del archivo csv a los tipos de mysql

    return jsonify({}), 201

