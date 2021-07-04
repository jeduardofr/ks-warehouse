import functools
import pandas as pd
from sqlalchemy.types import String, Integer, Date, DATETIME, Float

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

    db = get_db()

    db.execute("drop table if exists projects")

    data.to_sql(
        "projects", # Nombre de la tabla
        con=db, # Conexión a la base de datos
        dtype=map_columns_to_types) # Mapeo de las columnas del archivo csv a los tipos de mysql

    return jsonify({}), 201

