# from flask_sqlalchemy import SQLAlchemy
from pybo.connect_db import db


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject= db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

 

    