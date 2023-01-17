from flask import Flask, render_template, request
import sqlite3
import pandas as pd


def get_db(db_name):
    return sqlite3.connect(db_name)


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


app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Hello world"


@app.route('/sql')
def index():
    return render_template('index.html')


@app.route('/command', methods=['POST'])
def command():
    # render_template('index.html')
    return "TEST" + request.form.get('command')


@app.route('/data')
def data_page():
    return render_template('data.html')


# POST 받았을 때만 제한적으로 /dbsql을 라우팅할 때 아래  코드를 실행
@app.route('/dbsql', methods=["POST"])
def sql_test():
    if request.method == 'POST':
        db_name = request.form.get('db_name')
        sql_command = request.form.get('sql')

        conn = get_db(db_name)

        output, status = exe_sql(conn, sql_command)
        if status == 1:
            # 잘 처리됨
            return render_template('data.html', label="정상 작동", output=output)

        else:
            return render_template('data.html', label="오류 발생", output=None)


if __name__ == "__main__":
    app.run(debug=True)

# 가상환경 활성화 : .\flask_env\Scripts\Activate.ps1   (ps1은 powershell이라서)
# python .app/py3
# ctrl+shift+r :강제새로고침
