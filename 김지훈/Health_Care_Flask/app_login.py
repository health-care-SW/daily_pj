from flask import Flask, render_template, request, redirect, url_for, session, g, jsonify
import User
from datetime import timedelta

from __main__ import app

app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=3)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == 'POST':
        user_name = request.form['user_name']
        user_pw = request.form['user_password']
        user = User.select_user_with_name(user_name)

        if user != None and user.user_password == user_pw:
            session['username'] = user_name
            #return jsonify({"result" : "fail"})
            return redirect(url_for("hello"))

        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('hello'))

@app.before_request
def load_logged_in_user():
    user_name = session.get('username')
    print(session)
    if user_name is None:
        g.user = None
    else:
        g.user = User.select_user_with_name(user_name)
    
    print(g.user)



