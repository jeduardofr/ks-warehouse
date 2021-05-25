
from flask import Flask, render_template, request
from database import truncate_and_import_csv
from sqlalchemy import create_engine

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('upload-csv-form.html')

@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    truncate_and_import_csv('ks-projects/ks-projects-201801.csv')
    return "Subido con exito"

app.run()
