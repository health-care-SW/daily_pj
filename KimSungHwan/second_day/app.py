from flask import Flask, render_template, request
import sqlite3
import pymysql
import pandas as pd

app = Flask(__name__)

def get_db(db_name):
    # 디비 연결(sqlite3)
    # return sqlite3.connect(db_name)
    
    # 디비 연결(mysql)
    return pymysql.connect(
                    host='localhost',
                    port=3306,
                    user='root',
                    passwd='ksh0213',
                    db=db_name,
                    charset='utf8')

# sql 실행
def execute_sql(db_name, command):
    # 실행 시 예외처리
    try:
        # db를 커넥션을 가져옴
        conn = get_db(db_name)
        # db 탐색을 위한 커서를 만듦
        cursor = conn.cursor()
        # 커서를 통해 명령을 실행
        cursor.execute(command)
        # 결과를 저장
        conn.commit()
        
        # 셀렉트 문 일때
        if command.split()[0].lower() == 'select':
            # 쿼리를 실행해서 read_sql_query를 통해 DataFrame으로 바꿈
            df = pd.read_sql_query(command, conn, index_col=None)
            # df를 html 형식으로 바꿈 (table)
            html = df.to_html()
            conn.close()
            # 반환
            return html, 1
        conn.close()
        return True, 1    
    except Exception as e:
        return None, e


@app.route('/data')
def data():
    return render_template("data.html")

# 디비 실행 페이지
@app.route('/dbsql', methods=["POST"])
def sql_test():
    # POST (데이터 받기)로 데이터를 받으면
    if request.method == "POST":
        # 폼으로 부터 데이터 받음
        db_name = request.form.get("db_name")
        sql_command = request.form.get("sql")
    
        # sql 실행
        output, status = execute_sql(db_name, sql_command)
        
        # 실행 후 결과에 따라 정상, 오류, sql query html 결과 파싱
        if output != None: # 정상처리
            # select 문 일 때 output을 표현
            if sql_command.split()[0].lower() == 'select':
                return render_template("data.html", label="정상", output = None) + output
            # select문이 아니면 표현 안함  -- 이 조건을 처리하지 않으면 에러 발생 bool + str exception
            else: 
                return render_template("data.html", label="정상", output = None)
        elif output == None: # 오류 발생
            return render_template("data.html", label="오류 발생" + str(status), output=None)

    return render_template("data.html")


@app.route('/')
def hello_world():
    return "<a href='/sql' style='display:block;'>sql</a> <a href='/data'>dbsql</a>"

@app.route('/sql')
def index():
    return render_template("index.html")

@app.route('/command', methods=['POST','GET'])
def command():
    if request.method == 'POST':
        string = request.form.get('first_test')
        ll = list(string)
        res = "잘못된 형식"
        try:
            if ll[1] == '+':
                res = int(ll[0]) + int(ll[2])
            elif ll[1] == '-':
                res = int(ll[0]) - int(ll[2])
            elif ll[1] == '*':
                res = int(ll[0]) * int(ll[2])
            elif ll[1] == '/':
                res = int(ll[0]) / int(ll[2])
        except:
            pass    
        return render_template("index.html", result=res)
        # return "test "+ string


if __name__ == "__main__":
    app.run(debug=True)