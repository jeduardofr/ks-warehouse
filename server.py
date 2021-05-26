import os
from flask import Flask, render_template, request, jsonify
from database import truncate_and_import_csv
from sqlalchemy import create_engine

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('upload-csv-form.html')

@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    temporal_file = 'tmp.csv'

    uploaded_file = request.files['file']
    uploaded_file.save(temporal_file)

    truncate_and_import_csv(temporal_file)

    os.remove(temporal_file)

    return jsonify({}), 201

if __name__ == "__main__":
    app.run()
