from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from flask_bcrypt import Bcrypt
from api import board
from classification import board2
from community import board3
import pymysql
import pandas as pd
import os
from Database import Database

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.register_blueprint(board)
app.register_blueprint(board2)
app.register_blueprint(board3)

app.secret_key = 'tjdnf'
app.config['SESSION_TYPE'] = 'filesystem'

def get_app():
    return app

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico')

@app.route("/")
def main():
    if session.get("login"):
        print("session exist")
    else:
        print("session not exist")
    return render_template("index.html")

@app.route("/signin")
def sign_in():
    return render_template("signin.html")

@app.route("/check_dup", methods=["POST"])
def check_duplication():
    is_dup = False
    if request.method == "POST":
        id = request.form.get("inputID")
        if id == "":
            return render_template("signin.html",label="아무것도 입력되지 않았습니다. 입력해주세요",id= None, dup=False)
        conn = Database.get_db()
        cursor = conn.cursor()
        sql = "select * from user;"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            if row[2] == id:
                is_dup = True
                break
        if is_dup:
            return render_template("signin.html",label="중복된 아이디입니다. 다른 아이디를 사용해주세요",id= None, dup=False)
        else:
            return render_template("signin.html",label="사용 가능한 아이디입니다",id=id,dup=True)

@app.route("/signin_process",methods=["POST"])
def sign_in_process():
    if request.method == "POST":
        id = request.form.get("inputID")                
        pwd = request.form.get("inputPassword")  
        crypted_pwd = bcrypt.generate_password_hash(pwd.encode('utf-8'))     
        email = request.form.get("inputEmail")                
        phone_num = request.form.get("inputPhoneNum")         
        try:
            conn = Database.get_db()
            cursor = conn.cursor()
            sql = "insert into user values(%s,%s,%s,%s);"
            cursor.execute(sql, (id, crypted_pwd, email, phone_num))
            conn.commit()
            return redirect(url_for("main", label="회원가입 성공! 로그인해주세요"))
        
        except Exception as e:
            return redirect(url_for("main", label="오류 발생"))



if __name__ == "__main__":
    app.run(debug=True)