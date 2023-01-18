from flask import Flask, render_template, request, redirect, url_for,jsonify, Blueprint, session, g
from flask_bcrypt import Bcrypt
from model import User
import json
from Database import Database

board = Blueprint('board',__name__)
bcrypt = Bcrypt()

@board.before_app_request
def load_logged_in_user():
    user_id = session.get('login')
    if user_id is None:
        g.user = None
    else:
        g.user = User.find(user_id)


@board.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("index.html")
    else:
        user_id = request.form['id']
        user_pw = request.form['pwd']
        # data = json.loads(request.data)
        # user_id = data.get('id')
        # user_pw = data.get('pwd')
        try:
            user = User.find(user_id)
        except:
            return jsonify({"reesult":"fail"})
        if user is not None:
            if bcrypt.check_password_hash(user.user_pw, user_pw):
                session['login'] = user.user_id
                return redirect("/main")
            else:
                return jsonify({"reesult":"fail"})
        else:
            return jsonify({"result":"fail"})


@board.route("/logout",methods=['GET'])
def logout():
    if request.method == 'GET':
        if session.get("login"):
            print("session exist")
        else:
            print("session not exist")
        session["login"] = None
        return redirect('/')

@board.route("/main", methods=["GET","POST"])
def main():
    if request.method == "POST" or request.method == "GET":
        return render_template("main.html")
