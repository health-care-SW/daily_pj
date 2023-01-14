from flask import Flask, render_template, request
import sqlite3
import pandas as pd

# db 객체를 받아 사용하는 함수


def get_db(db_name):
    return sqlite3.connect(db_name)


def exe_sql(conn, command: str):

    try:
        conn.execute(command)
        conn.commit()
        # db에 명령을 보내고 동기화(?)

        # 명령어의 맨 앞에 lower(소문자)를 적용해서
        # select일 경우의 처리
        if command.split()[0].lower() == 'select':
            df = pd.read_sql(command, conn, index_col=None)
            df_html = df.to_html()  # 데이터프레임을 html 객체로 변환
            return df_html, 1  # 제대로 실행됐다면 1 리턴
    except:
        return None, 0  # 아니라면 0 리턴


app = Flask(__name__)

# 데코레이터. 루트 호출시 아래 코드를 실행시킴
@app.route('/')
def hello_world():
    return "Hello World"


@app.route('/sql')
def index():
    return render_template('index.html')


@app.route('/command', methods=['POST'])
def command():
    return "Test" + request.form.get('first_test')


@app.route('/data')
def data_page():
    return render_template('data.html')


@app.route('/dbsql', methods=["POST"])
def sql_test():
    if request.method == 'POST':
        db_name = request.form.get('db_name')
        sql_command = request.form.get('sql')

        conn = get_db(db_name)

        output, status = exe_sql(conn, sql_command)
        if status == 1:
            return render_template('data.html', label='정상 작동', output=output)
        else:
            return render_template('data.html', label="오류 발생", output=None)
    else:
        return render_template('data.html')


if __name__ == "__main__":
    app.run(debug=True)
