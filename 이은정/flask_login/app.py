import pymysql
from flask import Flask, send_from_directory
from api import board
from db_connect import db
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.register_blueprint(board)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://hchang:devpass@127.0.0.1:3306/board"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'ekdwls'

db.init_app(app)
bcrypt = Bcrypt(app)

if __name__ == '__main__':
    app.run(debug=True)
