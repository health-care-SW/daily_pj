from flask import Flask, redirect, request, render_template, jsonify, Blueprint, session, g
from models import User, db
from flask_bcrypt import Bcrypt
from datetime import timedelta

board = Blueprint('board', __name__)
bcrypt = Bcrypt()

# before_app_request를 이용해 로그인한 사용자를 확인하는 기능을 추가하세요.
app = Flask(__name__)


@board.before_app_request
def load_logged_in_user():
    user_id = session.get('login')
    if user_id is None:
        g.user = None
    else:
        g.user = db.session.query(User).filter(User.id == user_id).first()


def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)


@board.route("/")
def home():
    return render_template("base.html")

# 회원가입


@board.route("/join", methods=["GET", "POST"])
def join():
    if request.method == 'GET':
        return render_template('join.html')
    else:
        data = request.get_json()
        user_id = data['user_id']
        user_pw = data['user_pw']
        print(user_id)
        print(user_pw)
        pw_hash = bcrypt.generate_password_hash(user_pw)

        user = User(user_id, pw_hash)
        db.session.add(user)
        db.session.commit()
        return jsonify({"result": "success"})

# 로그인 기능


@board.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        data = request.get_json()
        user_id = data['user_id']
        user_pw = data['user_pw']

        user = User.query.filter(User.user_id == user_id).first()

        # 처음 실행 되었을시
        if user is not None:
            if bcrypt.check_password_hash(user.user_pw, user_pw):
                session['login'] = user.id
                return jsonify({"result": "success"})
            else:
                return jsonify({"reesult": "fail"})
        else:
            return jsonify({"result": "fail"})

# 로그아웃


@board.route("/logout")
def logout():
    session['login'] = None
    return redirect("/")
