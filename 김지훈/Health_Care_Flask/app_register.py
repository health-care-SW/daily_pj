from flask import Flask, render_template, request, redirect, url_for, g
import User

from __main__ import app

@app.route('/register')
def register():
    #이미 로그인 했다면 메인페이지
    if g.user != None:
        return redirect(url_for("hello"))

    return render_template("register.html")


@app.route('/register_process', methods=["POST"])
def register_process():
    userName = request.form.get('user_name')
    userPw = request.form.get('user_password')
    userEmail = request.form.get('user_email')
    user = User.User(userName, userPw, userEmail)
    User.insert_user(user)
    return redirect(url_for('index'))
