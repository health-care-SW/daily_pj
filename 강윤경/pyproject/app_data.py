'''
SQL 처리
'''

from flask import Flask, render_template, request
import sqlite3
import pandas as pd

# blueprint
from flask import Blueprint
bp = Blueprint('data', __name__, url_prefix = '/data')


'''
함수
'''

# DB 연결
def get_db(db_name):
    return sqlite3.connect(db_name)

# DB에 command (sql)
def sql_command(conn, command):

    try :

        conn.execute(command)
        conn.commit()
        # 소문자 변환
        command = command.lower()

        # select 입력시
        if "select" in command:
            # 빈칸 기준으로 command 나눠 리스트 저장
            command_split = command.split(" ")
            # 리스트에서 from 다음 단어 가져오기 (command)
            select_command = "SELECT * FROM " + command_split[command_split.index("from")+1]
            df = pd.read_sql(select_command, conn, index_col=None)
            # dataframe html로 변환
            html = df.to_html()

            conn.close()

            return html, 1

        conn.close()

        return True, 1

    except Exception as exception:

        conn.close()

        return False, exception


'''
플라스크
'''

# /index
@bp.route("/")
def index():
    return render_template('data.html')

# /dbsql
@bp.route('/dbsql', methods=['POST'])
def sql_processing():
    if request.method == 'POST':

        con = get_db(request.form.get('db_name'))
        sql = request.form.get('sql')
        result_sql, excep = sql_command(con, sql)

        if result_sql == False :
            return render_template('data.html', label="비정상" + str(excep))

        elif result_sql == True :
            return render_template('data.html', label="정상 작동")

        else :
            result_sql = "<html><body> " + result_sql + "</body></html>"
            return result_sql
