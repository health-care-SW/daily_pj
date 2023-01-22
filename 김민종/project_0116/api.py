from flask import render_template, request, redirect, url_for,jsonify, Blueprint, session, g
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

@board.route("/signin")
def sign_in():
    return render_template("signin.html")

@board.route("/check_dup", methods=["POST"])
def check_duplication():
    is_dup = False
    if request.method == "POST":
        id = request.form.get("inputID")
        if id == "":
            return render_template("signin.html",label="아무것도 입력되지 않았습니다. 입력해주세요",id= None, dup=False)
        sql = "select * from user;"
        cursor = Database().execute_query(sql)
        rows = cursor.fetchall()
        for row in rows:
            if row[0] == id:
                is_dup = True
                break
        if is_dup:
            return render_template("signin.html",label="중복된 아이디입니다. 다른 아이디를 사용해주세요",id= None, dup=False)
        else:
            return render_template("signin.html",label="사용 가능한 아이디입니다",id=id,dup=True)

@board.route("/signin_process",methods=["POST"])
def sign_in_process():
    if request.method == "POST":
        id = request.form.get("inputID")                
        pwd = request.form.get("inputPassword")  
        crypted_pwd = bcrypt.generate_password_hash(pwd.encode('utf-8'))     
        email = request.form.get("inputEmail")                
        phone_num = request.form.get("inputPhoneNum")         
        try:
            sql = "insert into user values(%s,%s,%s,%s);"
            Database().execute_query(sql, id, crypted_pwd, email, phone_num)
            return redirect(url_for("main", label="회원가입 성공! 로그인해주세요"))
        
        except Exception as e:
            return redirect(url_for("main", label="오류 발생"))




@board.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("index.html")
    else:
        data = json.loads(request.data)
        user_id = data.get('id')
        user_pw = data.get('pwd')
        try:
            user = User.find(user_id)
        except:
            return jsonify({"result":"fail"})
        if user is not None:
            if bcrypt.check_password_hash(user.user_pw, user_pw):
                session['login'] = user.user_id
                # return redirect("/main")
                return jsonify({"result":"success"})
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
