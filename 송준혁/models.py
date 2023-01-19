from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    # DB상 번호
    id = db.Column(db.Integer,  primary_key=True,
                   nullable=False, autoincrement=True)

    # 아이디, 비밀번호
    user_id = db.Column(db.String(100), nullable=False, unique=True)
    user_pw = db.Column(db.String(100), nullable=False)

    def __init__(self, user_id, user_pw):
        self.user_id = user_id
        self.user_pw = user_pw

    # 추후 front로 뺄 예정
    # 암호화

    # def set_password(self, password):
    #     self.password = generate_password_hash(password)

    # # 복호화
    # def check_password(self, password):
    #     return check_password_hash(self.password, password)


# 게시판
class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer,  primary_key=True,
                   nullable=False, autoincrement=True)
    author = db.Column(db.String(256), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, author, content):
        self.author = author
        self.content = content
