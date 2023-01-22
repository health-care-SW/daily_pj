from flask import Flask, render_template, request, Blueprint
# from flask_ngrok import run_with_ngrok

import os
import sqlite3
from PIL import Image
import pandas as pd

# blueprint
bp = Blueprint('main', __name__, url_prefix='/main')

# app = Flask(__name__)
# run_with_ngrok(app)

@bp.route('/')
def index():
    return render_template('main.html')
 
# @app.route('/about')
# def about():
#     return 'About project'

@bp.route('/get_selected_table', methods=["POST"])
def select_table():
      table_id = request.form.get('table_name')
      print(table_id)
      return render_template('main.html')

@bp.route('/get_column_name_change', methods=['POST'])
def column_name_change():
    bef_column_name = request.form.get('before_column_name')
    aft_column_name = request.form.get('after_column_name')

    print(bef_column_name)
    print(aft_column_name)

    return render_template('main.html')

@bp.route('/get_image_pre_status', methods=['POST'])
def image_preprocessing():
    if request.method == 'POST':
        print("0 = ", request.form.get('pre_toggle_0'))
        print("1 = ", request.form.get('pre_toggle_1'))
        print("2 = ", request.form.get('pre_toggle_2'))
    return render_template('main.html')

@bp.route('/upload_image', methods=['POST'])
def upload_image_file():
    if request.method == 'POST':

        file = request.files['uploaded_image']
        if not file: return render_template('main.html', label="No Files")
 
        return render_template('main.html', label=file)


# if __name__ == '__main__':
#     app.run(debug=True)