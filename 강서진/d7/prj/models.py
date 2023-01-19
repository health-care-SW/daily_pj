from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    user_email = db.Column(db.String(100), nullable=False, unique=True)
    user_pw = db.Column(db.String(100), nullable=False)
    pw_hash = db.Column(db.String(100), nullable=False)

    def __init__(self, username, user_pw, user_email, pw_hash):
        self.username = username
        self.user_email = user_email
        self.user_pw = user_pw
        self.pw_hash = pw_hash

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.String(256), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, nullable=True)

    # def __init__(self, title, author, content, created_at, modified_at):
    #     self.title = title
    #     self.author = author
    #     self.content = content
    #     self.created_at = created_at
    #     self.modified_at = modified_at
