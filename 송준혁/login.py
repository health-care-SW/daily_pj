from flask import Flask
from api import board
from api import *
from flask_bcrypt import Bcrypt
from models import *

import app_data
import app_image

app = Flask(__name__)
app.register_blueprint(board)
app.register_blueprint(app_data.board)
app.register_blueprint(app_image.board)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'ekdwls'

db.init_app(app)
db.app = app

# db생성
with app.app_context():
    db.create_all()

bcrypt = Bcrypt(app)

if __name__ == '__main__':
    app.run(debug=True)
