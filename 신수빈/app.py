from flask import Flask, render_template, request
import sqlite3
import pandas as pd
import os
from PIL import Image
import pymysql
from api import board
from db_connect import db
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.register_blueprint(board)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://hchang:devpass@127.0.0.1:3306/board"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'ekdwls'

# run_with_ngrok(app)

'''
이미지 처리 함수
'''

# 이미지의 사이즈 변환하는 함수
def image_resize(image, width, height):
        return image.resize((int(width), int(height)))

# 이미지를 회전 시키는 함수 (180도)
def image_rotate(image):
    return image.transpose(Image.ROTATE_180)

# 이미지 흑백 전환 함수
def image_change_bw(image):
    return image.convert('L')

'''
db 관련 함수
'''

#db가 없으면 생성, 존재하면 open
def get_db(db_name):
    return sqlite3.connect(db_name)

#sql 관련 명령어 실행
def exe_sql(conn, command: str):    
    try:
        conn.execute(command)
        conn.commit()
        
        if command.split()[0].lower() == 'select':
            df = pd.read_sql(command, conn, index_col=None)
            df_html = df.to_html()
            return df_html,1
        else: 
            return None, 1
    except:
        return None,0


@app.route("/")
def index():
    return render_template('index.html')

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
        return render_template('index.html', label=image_path)

@app.route('/get_column_name_change', methods=['POST'])
def column_name_change():
    # aft_column_name = request.form.values('after_column_name')
    bef_column_name = request.form.get('before_column_name')
    aft_column_name = request.form.get('after_column_name')

    print(bef_column_name)
    print(aft_column_name)

    return render_template('image.html')

@app.route('/get_image_pre_status', methods=["POST"])
def image_preprocessting():
    if request.method == 'POST':
        print("0=", request.form.get('pre_toggle_0'))
        print("1=", request.form.get('pre_toggle_1'))
        print("2=", request.form.get('pre_toggle_2'))
    return render_template('image.html')

@app.route('/get_selected_table', methods=['POST'])
def selected_table():
    text = request.form.get('table_name')
    print(text)
    return render_template('index.html')

@app.route('/get_selected_table2', methods=['POST'])
def selected_table2():
    text = request.form.get('textbox')

    return render_template('image.html', label=text)

@app.route('/upload_image', methods=['POST'])
def upload_image_file():
    if request.method == 'POST':
        file = request.files['uploaded_image']
        if not file: return render_template('image.html', label="No Files")
        label = file.filename
        file.save('static/'+label)

        return render_template('image.html', label=label)


@app.route('/about')
def about():
    return 'About Project' #render_template('about.html')


@app.route('/command',methods=['POST'])
def command():
    return "TEST" + request.form.get('first_test')

@app.route('/data')
def data_page():
    return render_template('data.html')

@app.route('/dbsql', methods=['POST'])
def sql_test():
    if request.method == 'POST':
        db_name = request.form.get('db_name')
        sql_command = request.form.get('sql')
        
        conn = get_db(db_name)

        output,status = exe_sql(conn, sql_command)
        if status ==1:
            # 잘 처리됨
            return render_template('data.html', label = "정상 작동", output=output)

        else:
            # 오류 발생
            return render_template('data.html', label = "오류 발생", output=None)
    else: return render_template('data.html')

if __name__ =="__main__":
    app.run()