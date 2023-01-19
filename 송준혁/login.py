import pymysql
from flask import Flask
from api import board
from api import db
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.register_blueprint(board)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://hchang:devpass@127.0.0.1:3306/board"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'ekdwls'

db.init_app(app)
bcrypt = Bcrypt(app)

if __name__ == '__main__':
    app.run(debug=True)
