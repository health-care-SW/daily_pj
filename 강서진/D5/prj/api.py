from flask import redirect, render_template, request, jsonify, Blueprint, session, g
from . import models
from . import db_connect
from flask_bcrypt import Bcrypt


board = Blueprint('board', __name__)
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

@board.route('/login', methods=["GET","POST"])
def login():
    # GET으로 접근 시 로그인 페이지로 이동
    if request.method=='GET':
        return render_template('login.html')

    # POST로 접근 시 
    else:
        user_id = request.form['user_id']
        user_pw = request.form['user_pw']
        user = User.query.filter(User.user_id == user_id).first()

        if user is not None:
            if bcrypt.check_password_hash(user.user_pw, user_pw):
                session['login'] = user.id
                return jsonify({"result":"success"})
            else:
                return jsonify({"result":"fail"})
        else:
            return jsonify({"result":"fail"})

@board.route("/logout")
def logout():
    session['login'] = None
    return redirect("/")

@board.route("/post", methods=["GET"])
def post():
    return render_template("index.html")