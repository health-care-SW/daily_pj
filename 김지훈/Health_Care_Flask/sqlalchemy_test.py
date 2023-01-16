from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "mariadb+pymysql://root:0000@localhost:3306/shopping_mall"
# initialize the app with the extension
db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'
    user_seq = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), unique=True, nullable=False)
    user_password = db.Column(db.String(50), nullable=False)
    user_email = db.Column(db.String(100), nullable=False)
    user_profile_image_url = db.Column(db.String(500))
    user_register_date = db.Column(db.DateTime(timezone=True), default=datetime.now())

    def __str__(self):
        return "user_seq:" + str(self.user_seq) + "\t user_name:" + self.user_name + "\t user_email:" + self.user_email 

def user_list():
    users = db.session.query(User).all()
    for user in users:
        print(user)
        


with app.app_context():
    db.create_all()
    user_list()