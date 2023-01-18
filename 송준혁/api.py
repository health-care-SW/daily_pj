from flask import Flask, redirect, request, render_template, jsonify, Blueprint, session, g
from models import User, Post
from db_connect import db
from flask_bcrypt import Bcrypt

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


@board.route("/")
def home():
    return render_template("base.html")


@board.route("/post", methods=["GET"])
def post():
    return render_template("index.html")


@board.route("/join", methods=["GET", "POST"])
def join():
    if request.method == 'GET':
        return render_template('join.html')
    else:
        user_id = request.form['user_id']
        user_pw = request.form['user_pw']
        pw_hash = bcrypt.generate_password_hash(user_pw)

        user = User(user_id, pw_hash)
        db.session.add(user)
        db.session.commit()
        return jsonify({"result": "success"})

# 로그인을 위한 login() 함수를 완성하세요.


@board.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        user_id = request.form['user_id']
        user_pw = request.form['user_pw']
        user = User.query.filter(User.user_id == user_id).first()

        if user is not None:
            if bcrypt.check_password_hash(user.user_pw, user_pw):
                session['login'] = user.id
                return jsonify({"result": "success"})
            else:
                return jsonify({"reesult": "fail"})
        else:
            return jsonify({"result": "fail"})

# 로그아웃을 위한 logout() 함수를 완성하세요.


@board.route("/logout")
def logout():
    session['login'] = None
    return redirect("/")

# 로그인 기능 함수


@app.route('/login', methods=['GET', 'POST'])
def login():
    user_id = request.form['user_id']
    user_pw = request.form['user_pw']

    if request.method == 'GET':
        render_template('login.html')

    elif request.method == 'POST':
        # 데이터 작성
        print()
