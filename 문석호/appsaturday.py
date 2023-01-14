from flask import Flask, render_template, request
import pandas as pd
import sqlite3

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
    except:
        return None, 0

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello, World!"

@app.route('/sql')
def index():
    return render_template('index.html')

@app.route('/data')
def data_page():
    return render_template('data.html')

@app.route('/dbsql', methods=["POST"])
def sql_test():
    if request.method=='POST':
        db_name = request.form.get('db_name')
        sql_command = request.form.get('sql')

        conn = get_db(db_name)

        ot, status = exe_sql(conn, sql_command)

        if status == 1:
            #처리됨
            return render_template('data.html', label = "정상 작동", output = ot)

        else:
            #처리 안됨
            return render_template('data.html', label = "오류 발생", output = None)
        # return db_name + sql_command
    else: 
        return data_page()

@app.route('/command', methods=['POST'])
def command():
    exp = request.form.get('first_test').split()
    i = 0
    # while i < len(exp):
         

    if len(exp)!=3:
        return "연산 1번만 가능"
    elif exp[1] == '+':
        return str(int(exp[0]) + int(exp[2])) 
    elif exp[1] == '-':
        return str(int(exp[0]) - int(exp[2]))
    elif exp[1] == '*':
        return str(int(exp[0]) * int(exp[2]))
    elif exp[1] == '/':
        if int(exp[2]) == 0:
            return "DIV 0 ERROR"
        else:
            return str(int(exp[0]) / int(exp[2]))
    else:
        return "TEXT"

if __name__=="__main__":
    app.run(debug=True)


from flask import Flask, render_template, request
from flask_ngrok import run_with_ngrok
import os
from PIL import Image

app = Flask(__name__)
run_with_ngrok(app)

'''
이미지 처리 함수
'''
def image_resize(image, width, height):
        return image.resize((int(width), int(height)))

def image_rotate(image):
    return image.transpose(Image.ROTATE_180)

def image_change_bw(image):
    return image.convert('L')

'''
플라스크
'''
@app.route("/index")
def index():
    return render_template('image.html')

@app.route('/image_preprocess', methods=['POST'])
def preprocessing():
    if request.method == 'POST':
        file = request.files['uploaded_image']
        if not file: return render_template('index.html', label="No Files")

        img = Image.open(file)

        is_rotate_180 = request.form.get('pre_toggle_0')
        is_change_bw = request.form.get('pre_toggle_1')
        is_change_size = request.form.get('pre_toggle_2')

        if is_rotate_180 == 'on':
            img = image_rotate(img)

        if is_change_bw == 'on':
            img = image_change_bw(img)

        if is_change_size == 'on':
            img = image_resize(img, request.form.get('changed_width'), request.form.get('changed_height'))

        img.save('result_image.png')

        src_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(src_dir, 'result_image.png')

        # 결과 리턴
        return render_template('image.html', label=image_path)

if __name__ == '__main__':
    app.run()
