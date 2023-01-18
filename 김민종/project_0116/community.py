from flask import Flask, render_template, request, redirect, url_for,jsonify, Blueprint, session, g
from model import User
from datetime import datetime
import json
import pymysql
import uuid
from Database import Database

board3 = Blueprint('board3',__name__)


@board3.before_app_request
def load_logged_in_user():
    user_id = session.get('login')
    if user_id is None:
        g.user = None
    else:
        g.user = User.find(user_id)

@board3.route("/community",methods=["GET","POST"])
def community():
    if request.method == "POST" or request.method == "GET":
        try:
            conn = Database.get_db()
            cursor = conn.cursor()
            sql = "select * from writing;"
            cursor.execute(sql)
            rows = cursor.fetchall()
            return render_template("community.html",result = rows)
        except Exception as e:
            return redirect(url_for("board3.community", label="오류 발생"))

    return render_template("community.html")

@board3.route("/write",methods=["GET", "POST"])
def write():
    now = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
    return render_template("write.html", time = now)

@board3.route("/write_process", methods=["POST"])
def write_process():
    if request.method == "POST":

        title = request.form.get("title")
        desc = request.form.get("description")
        date = request.form.get("date")
        writer = request.form.get("name")
        id = str(uuid.uuid1().hex)
        file = request.files['filename']
        file.save('./static/assets/images/'+id+".png")
        try:
            conn = Database.get_db()
            cursor = conn.cursor()
            sql = "insert into writing values(%s,%s,%s,%s,%s);"
            cursor.execute(sql, (title, desc, date, writer, id))
            conn.commit()
            return redirect(url_for("board3.community"))
            
        except Exception as e:
            return redirect(url_for("board3.community", label="오류 발생"))


@board3.route("/detail", methods=["GET"])
def detail():
    if request.method == "GET":
        writing_id = request.args.get("writing_id")
        try:
            conn = Database.get_db()
            cursor = conn.cursor()
            sql = "select * from writing where id=%s;"
            cursor.execute(sql,(writing_id))
            row = cursor.fetchall()
            return render_template("detail.html",detail=row[0])
        except Exception as e:
            pass