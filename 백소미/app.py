from flask import Flask, render_template, request
import sqlite3
import pandas as pd

def get_db(db_name):
    return sqlite3.connect(db_name) #db_name을 받아서 사용

def exe_sql(conn, commend):
    try:
        conn.execute(command)
        conn.commit() #변화된 거 처리

        if command.split()[0].lower() == 'select':
            df = pd.read_sql(command, conn, index_col=None) #판다스가 데이터프래임 반환
            df_html = df.to_html()
            return df_html, 1
    except:
        return None, 0
#2:09:48
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello world"

@app.route('/sql')
def index():
    return render_template('index.html')

@app.route('/command', methods=['POST'])
def command():    
    return "TEST" + request.form.get('first_test') # render_template('index.html')

@app.route('/data')
def data_page():
    return render_template('data.html')

@app.route('/dbsql', methods=['POST'])
def sql_test():
    if request.method == 'POST':
        db_name = request.form.get('db_name')
        sql_command = request.form.get('sql')

        conn = get_db(db_name) #연결된 db받아옴

        output, status = exe_sql(conn, sql_command)
        if status == 1:
            #잘 처리됨
            return render_template('index.html', label=image_path)

        else:
            #오류 발생
            return render_template('data.html', label = "오류 발생")


if __name__=="__main__":
    app.run(debug=True)