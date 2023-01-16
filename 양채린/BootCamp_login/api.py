from flask import redirect, request, render_template, jsonify, Blueprint, session, g
from models import User, Post
from db_connect import db
from flask_bcrypt import Bcrypt

board = Blueprint('board', __name__)
# password-hashing function이다.
# Blowfish 암호를 기반으로 설계된 암호화 함수이며 현재까지 사용중인 가장 강력한 해시 메커니즘 중 하나이다.
# 보안에 집착하기로 유명한 OpenBSD에서 사용하고 있다.
# .NET 및 Java를 포함한 많은 플랫폼,언어에서 사용할 수 있다.
bcrypt = Bcrypt()

# before_app_request를 이용해 로그인한 사용자를 확인한다.
# flask.g 변수에는 모든 전역 정보가 포함돼있고, 원하는 어떤 속성이든 여기에 설정할 수 있다.
@board.before_app_first_request
def load_logged_in_user():
    user_id = session.get('login')
    if user_id is None:
        g.user = None
    else: 
        g.user = db.session.query(user).filter(User.id == user_id).first()

@board.route('/')
def home():
    return render_template("base.html")

@board.route('/post', methods=['get'])
def post():
    return render_template("index.html")

@board.route('/join', methods=['get', 'post'])
def join():
    if request.method == 'get':
        return render_template('join.html')
    else:
        user_id = request.form['user_id']
        user_pw = request.form['user_pw']
        pw_hash = bcrypt.generate_password_hash(user_pw)

        user = User(user_id, pw_hash)
        db.session.add(user)
        db.session.commit()
        return jsonify({"result": "session"})

# 로그인을 위한 login() 함수 완성
@board.route('/login', methods=['get', 'post'])
def login():
    if request.method == 'get':
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
                return jsonify({"result": "fail"})
        else:
            return jsonify({"result": "fail"})

# 로그아웃을 위한 logout() 함수 완성
@board.route('/logout')
def logout():
    session['login'] = None
    return redirect('/')