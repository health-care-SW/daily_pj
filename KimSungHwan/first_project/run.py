import pymysql
from flask import Flask
from api import board
from db_connect import db
from flask_bcrypt import Bcrypt
from config import DB_URL
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

login_manager = LoginManager()

app = Flask(__name__)
app.register_blueprint(board)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:ksh0213@127.0.0.1:3306/flask_test"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'tjdghks'

db.init_app(app)
# login_manager.init_app(app)
bcrypt = Bcrypt(app)




if __name__ == '__main__':
    app.run(debug=True)
