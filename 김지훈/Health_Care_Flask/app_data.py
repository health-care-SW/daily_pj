from flask import Flask, render_template, request, redirect, url_for, g

import sqlite3
import pandas as pd

from __main__ import app

def get_db(db_name):
    return sqlite3.connect(db_name)

def exe_sql(conn, command):

    try:
        conn.execute(command)
        conn.commit()

        if command.split()[0].lower() == 'select':
            df = pd.read_sql(command, conn, index_col = None)
            conn.close()
            return df, 1
        else:
            return None, 0
    except:
        return None, 0




@app.route('/sql')
def sqlIndex():
    #로그인하지 않았다면 메인페이지
    if g.user == None:
        return redirect(url_for("hello"))

    return render_template("/sql_command.html")

@app.route('/command', methods=['POST'])
def command():
    getStr = request.form.get('first_test')

    if '+' in getStr: 
        a,b = getStr.split('+')
        res = int(a) + int(b)

        return 'command: ' + str(res)
    else:
        return 'invalid command'

@app.route('/data')
def data_page():
    return render_template("/data.html")



@app.route('/dbsql', methods=['POST'])
def sql_test():
    if request.method=='POST':
        db_name = request.form.get('db_name')
        sql_command = request.form.get('sql')

        conn = get_db(db_name)
        output, status= exe_sql(conn, sql_command)

        if status == 1:
            # sql 실행 성공
            return render_template('data.html', label = "정상 작동", outputs=[output.to_html(classes='data')])
            #return output

        else:
            # sql 실행 오류
            return render_template('data.html', label = "오류 발생" ,output = None
)
