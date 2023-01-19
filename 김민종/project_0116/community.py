from flask import render_template, request, redirect, url_for, Blueprint, session, g
from model import User
from datetime import datetime
from Database import Database
from util import str2time
from util import check_session
import uuid
import os


commu = Blueprint('community',__name__)


@commu.before_app_request
def load_logged_in_user():
    user_id = session.get('login')
    if user_id is None:
        g.user = None
    else:
        g.user = User.find(user_id)

@commu.route("/community",methods=["GET","POST"])
def community():
    if request.method == "POST" or request.method == "GET":
        try:
            sql = "select * from writing;"
            cursor = Database().execute_query(sql)
            rows = cursor.fetchall()
            ll = str2time(rows, 2)
            return render_template("/board/community.html",result = ll)
        except Exception as e:
            return redirect(url_for("community.community", label="오류 발생"))

    return render_template("/board/community.html")

@commu.route("/write",methods=["GET"])
def write():
    s = session['login']
    if check_session(s):
        now = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
        return render_template("/board/write.html", time = now)
    else:
        return redirect(url_for("community.community",error=1))

@commu.route("/write_process", methods=["GET","POST"])
def write_process():
    if request.method == "POST" and check_session(session['login']):
        title = request.form.get("title")
        desc = request.form.get("description")
        date = request.form.get("date")
        writer = request.form.get("name")
        id = str(uuid.uuid1().hex)
        file = request.files['filename']
        if file.filename != '':
            file.save('./static/assets/images/'+id+".png")
        try:
            sql = "insert into writing values(%s,%s,%s,%s,%s);"
            Database().execute_query(sql, title, desc, date, writer, id)
            return redirect(url_for("community.community"))
            
        except Exception as e:
            return redirect(url_for("community.community", label="오류 발생"))
    else:
        return redirect(url_for("community.community",error=2))


@commu.route("/detail", methods=["GET"])
def detail():
    if request.method == "GET":
        writing_id = request.args.get("writing_id")
        try:
            sql = "select * from writing where id=%s;"
            sql_reply = "select * from reply where reply_id=%s;"
            cursor = Database().execute_query(sql, writing_id)
            cursor_reply = Database().execute_query(sql_reply, writing_id)
            row = cursor.fetchall()
            row_reply = cursor_reply.fetchall()
            ll = str2time(row_reply, 3)
            return render_template("/board/detail.html",detail=row[0],replies=ll)
        except Exception as e:
            return redirect("community")

@commu.route("/reply", methods=["GET","POST"])
def reply():
    if request.method == "POST" and check_session(session['login']) :
        reply = request.form.get('reply')
        reply_writer = session['login']
        reply_date = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
        reply_id = request.args.get("reply_id")
        try:
            sql = "insert into reply values(%s,%s,%s,%s);"
            Database().execute_query(sql, reply_id, reply_writer, reply, reply_date)
            return redirect("detail?writing_id=%s"%(reply_id))
        except:
            return redirect("detail?writing_id=%s"%(reply_id))
    else:
        return redirect(url_for("community.community",error=2))

@commu.route("/delete_reply", methods=["GET","POST"])
def delete_reply():
    if request.method == "POST" and check_session(session['login']):
        writer = request.args.get("writer")
        reply = request.args.get("reply")
        time = request.args.get("time")
        reply_id = request.args.get("id")
        try:
            sql = "delete from reply where reply_writer=%s and reply=%s and reply_date=%s;"
            Database().execute_query(sql, writer, reply, time)
            return redirect("detail?writing_id=%s"%(reply_id))
        except:
            return redirect("detail?writing_id=%s&error=1"%(reply_id))
    else:
        return redirect(url_for("community.community",error=2))

@commu.route("/update_reply", methods=["GET","POST"])
def update_reply():
    if request.method == "POST" and check_session(session['login']):
        writer = request.args.get("writer")
        time = request.args.get("time")
        id = request.args.get("id")
        reply = request.form.get("update")
        updated_time = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
        
        try:
            conn = Database().get_db()
            cursor = conn.cursor()
            sql = "update reply set reply=%s, reply_date=%s where reply_id=%s and reply_writer=%s and reply_date=%s;"
            cursor.execute(sql,(reply, updated_time, id, writer, time))
            conn.commit()
            return redirect("detail?writing_id=%s"%(id))
        except:
            return redirect("detail?writing_id=%s&error=1"%(id))
    else:
        return redirect(url_for("community.community",error=2))

@commu.route("/delete_writing", methods=["GET","POST"])
def delete_writing():
    if request.method == "POST" and check_session(session['login']):
        try:
            id = request.get_data()
            decoded_id = id.decode('utf-8')
            sql = 'delete from writing where id=%s;'
            Database().execute_query(sql, decoded_id)
            file_path = './static/assets/images/'+decoded_id+'.png'
            if os.path.isfile(file_path):
                os.remove(file_path)
            return redirect("community")
        except:
            return redirect("community?error=1")   
    else:
        return redirect(url_for("community.community",error=2))