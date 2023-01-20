# main file
# []
# ctrl+B
# 터미널 껐다켰다? ctrl+ `

from flask import Flask, render_template, request
import sqlite3
import pandas as pd

# db 가져오는 함수: db명 전달 -> 해당 db 반환
def get_db(db_name): 
    return sqlite3.connect(db_name)

# sql 명령어 처리 함수
def exe_sql(conn, command: str):
    try:
        conn.execute(command)
        conn.commit()

        if command.split()[0].lower() == 'select':
            df = pd.read_sql(command, conn, index_col=None)
            df_html = df.to_html()
            return df_html, 1
        else:
            return None, 1
    except:
        return None, 0

app = Flask(__name__) # Flask 클래스를 app 인스턴스에 받기

@app.route('/')
def hello_world():
    return "Hello World"

@app.route('/sql')
def index():
    return render_template("index.html")

@app.route('/command', methods=['POST'])
def test():
    return "TEST"+request.form.get('first_test')

@app.route('/data')
def data_page():
    return render_template('data.html')

@app.route('/dbsql', methods=['POST'])
def sql_test():
    if request.method=='POST':

        db_name = request.form.get('db_name')
        sql_command = request.form.get('sql')
        
        conn = get_db(db_name)
        
        output1, status = exe_sql(conn, sql_command)
        if status == 1:
            # 정상 처리
            # return db_name + sql_command
            # print(output1)
            output2 = "<div>" + output1 + "</div>"
            return render_template('data.html', label = "정상 작동", output = output2)
        else:
            # 오류 발생
            return render_template('data.html', label = "오류 발생", output = None)
    else:
        return render_template('data.html')
        

if __name__ == "__main__":
    app.run(debug=True)
