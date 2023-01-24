import os
from flask import redirect, render_template, request, jsonify, Blueprint, session, g
from flask_bcrypt import Bcrypt
from . import models
from . import db_connect


board = Blueprint('board_j', __name__)
bcrypt = Bcrypt()

db = db_connect.db
User = models.User


# 세션에 로그인 기록이 있나 확인는지 사용자를 확인하는 기능
@board.before_app_request
def load_logged_in_user():
    user_id = session.get('login')
    if user_id is None:
        g.user = None
    else:
        g.user = db.session.query(User).filter(User.id == user_id).first()

# base.html이 메인
@board.route("/")
def home():
    return render_template("base.html")

# 회원가입 페이지
@board.route("/join", methods=["GET", "POST"])
def join():
    # get으로 접근
    if request.method=="GET":
        return render_template("join.html")

# post로 접근
    else:
        # join 사이트에서 user_id, user_pw 받아옴
        user_id = request.form['user_id']
        user_pw = request.form['user_pw']
        # pw_hash = bcrypt.generate_password_hash(user_pw)

        # db 객체에 user_id, user_pw 넣어서 user에 할당
        user = User(user_id, user_pw)
        # db 에 user 추가
        db.session.add(user)
        db.session.commit()

        return jsonify({"result":"success"}), redirect('/')
