from flask import Flask, render_template, request, session, redirect, Blueprint
#from flask_ngrok import run_with_ngrok
import os
from datetime import datetime
from PIL import Image
import pandas as pd
import sqlite3
from pybo.test import create_app
from pybo.models import Question
from pybo.test import bp

app = create_app()
#run_with_ngrok(app)

def get_db(db_name):
     print(db_name)
     return sqlite3.connect(db_name)



def sql_command(conn, command):

    try :

        conn.execute(command)
        conn.commit()
        command = command.lower()

        if "select" in command:

            command_split = command.split(" ")
            select_command = "SELECT * FROM " + command_split[command_split.index("from")+1]
            df = pd.read_sql(select_command, conn, index_col=None)
            html = df.to_html()

            conn.close()

            return html, 1

        conn.close()

        return True, 1

    except Exception as exception:

        conn.close()

        return False, exception

#-------------------------------------

def select():
    con = get_db('./' + 'test_')
    cursor = con.cursor()
    sql = "select * from board order by timestamp desc"
    cursor.execute(sql)
    rows = cursor.fetchall()
    con.close()
    return rows



#-----------------------------------------------

@bp.route('/')
def index():
    question_list = Question.query.order_by(Question.create_date.desc())
    return render_template('question/question_list.html', question_list=question_list)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question)


@app.route('/')
def index():
    return render_template('login_form.html')

#로그인  
@app.route('/login_proc', methods=['POST'])
def login_proc():
    

        id = request.form['id']
        passwd = request.form['pwd']
        

        con = get_db('./' + 'test_')
        cursor = con.cursor()
        sql = "select id, username, passwd from user where id = " + "'" + id + "'" 
        cursor.execute(sql)
        rows = cursor.fetchall()
        for rs in rows:
            if id == rs[0] and passwd == rs[2]:
                session['id'] = id
                sql2 = "select * from board order by timestamp desc"
                cursor.execute(sql2)
                rows2 = cursor.fetchall()
                lists = rows2
                return render_template('image.html', lists=lists)
            else:
                return redirect('login_form.html')
        
    
app.secret_key = 'sample_secret_key'


#회원가입 
@app.route('/register_proc', methods=['POST'])
def register_proc():
    if request.method == 'POST':

        id = request.form['id']
        username = request.form['name']
        passwd = request.form['pwd']
        

        con = get_db('./' + 'test_')
        cursor = con.cursor()
        sql = "insert into user values('" + id + "','" +username+ "','" +  passwd +"')"
        cursor.execute(sql)
        con.commit()
        con.close()

        
        session['id'] = id
        return render_template('image.html')

app.secret_key = 'sample_secret_key'

#이미지 업로드
@app.route('/image_upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['uploaded_image']
        if not file: return render_template('index.html', label="No Files")
        img = Image.open(file)

        session['title'] = request.form['title']
        now = datetime.now()
        now_text = now.strftime("%Y/%m/%d, %H:%M:%S")

        con = get_db('./' + 'test_')
        cursor = con.cursor()
        sql = "insert into board values('" +session['id']+  "','" +  session['title'] + "','" + now_text +"')"
        cursor.execute(sql)
        con.commit()

        sql2 = "select * from board order by timestamp desc"
        cursor.execute(sql2)
        rows = cursor.fetchall()
        lists = rows
        con.close()

        img.save('static/result_image.png')
        
        return render_template('lists.html', lists=lists)

#-------------------------------------------
#보드게시판 리스트
@app.route('/lists')
def lists():
    lists = select()
    return render_template('lists.html', lists=lists)
#------------------------------------------
# 데이터베이스
'''
File upload
'''


@app.route('/dbsql', methods=['POST'])
def sql_processing():
    if request.method == 'POST':

        con = get_db('./' + 'test_')
        sql = request.form.get('sql')
        result_sql, excep = sql_command(con, sql)

        if result_sql == False :
            return render_template('data.html', label="비정상" +  str(excep))

        elif result_sql == True :
            return render_template('data.html', label="정상 작동")

        else :
            result_sql = "<html><body> " + result_sql + "</body></html>"
            return result_sql

if __name__ == '__main__':
    app.run(debug=True)