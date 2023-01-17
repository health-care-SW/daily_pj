from flask import redirect, request, render_template, jsonify, Blueprint, session, g
from models import User, Post
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


board = Blueprint('board',__name__)
bcrypt = Bcrypt()

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

@board.route("/join",methods=["GET","POST"])
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
        return jsonify({"result":"success"})

@board.route("/login",methods=['GET','POST'])
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
                return jsonify({"result":"success"})
            else:
                return jsonify({"reesult":"fail"})
        else:
            return jsonify({"result":"fail"})


@board.route("/logout")
def logout():
    session['login'] = None
    return redirect("/")
