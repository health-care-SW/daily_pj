import pymysql
from flask_mysqldb import MySQL
from flask import Flask
from api import board
from db_connect import db
from flask_bcrypt import Bcrypt
from config import DB_URL, db

app = Flask(__name__)
app.register_blueprint(board)

app.config['MYSQL_HOST'] = db['host']
app.config['MYSQL_USER'] = db['user']
app.config['MYSQL_PASSWORD'] = db['password']
app.config['MYSQL_DB'] = db['database']
app.config['MYSQL_PORT'] = db['port']

mysql = MySQL(app)
bcrypt = Bcrypt(app)

if __name__ == '__main__':
    app.run(debug=True)
