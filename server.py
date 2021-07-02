# Desarrollado por:
# - Fuentes Rangel, Jesús Eduardo
# - López Barajas, Andrés Esaú
import os
from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine
from database import truncate_and_import_csv, database_connection

app = Flask(__name__)

# @@@: Authentication required
@app.route("/")
def index():
    return render_template('views/session/upload-csv-form.html')

# @@@: Authentication required
@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    temporal_file = 'tmp.csv'

    uploaded_file = request.files['file']
    uploaded_file.save(temporal_file)

    truncate_and_import_csv(temporal_file)

    os.remove(temporal_file)

    return jsonify({}), 201

@app.route('/login', methods=['GET'])
def login():
    return render_template('views/auth/login.html')

@app.route('/login', methods=['POST'])
def login_process():
    request

# @@@: Authentication required
@app.route('/table', methods=['GET', 'POST'])
def show_table():
    engine = create_engine(database_connection)
    rows = engine.execute("select * from projects limit 1000")
    print(rows)
    return render_template('views/session/show-table.html', rows=rows)


if __name__ == "__main__":
    app.run()
