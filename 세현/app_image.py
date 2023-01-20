from flask import Flask, render_template, request
import sqlite3
import pandas as pd
from flask_ngrok import run_with_ngrok

# from project.data import *
# from project.image import *
app = Flask(__name__)
# run_with_ngrok(app)

'''File upload
'''
# db 가져오는 함수: db명 전달 -> 해당 db 반환
def get_db(db_name): 
    return sqlite3.connect(db_name)

# sql 명령어 처리 함수
def exe_sql(conn, origin_column, new_column, db):
    try:
        command = "alter table" + db + "change" + origin_column + new_column + 컬럼타입 +";"
        conn.execute(command)
        conn.commit()

        select_command = "select * from" + db
        df = pd.read_sql(select_command, conn, index_col=None)
        df_html = df.to_html()
        return df_html, 1
    except:
        return None, 0



# 기본 페이지 ()
@app.route('/')
def index():
    return render_template('image.html')



# 테이블 받아오기
@app.route('/get_selected_table', methods=['POST'])
def selected_table():
    db_name = request.form.get('table_name')
    print(db_name)

    if request.method == 'POST':
        conn = get_db(db_name)
        output, status = exe_sql(conn)


    return render_template('index.html')



# 칼럼 이름 변경
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

@app.route('/get_selected_table2', methods=['POST'])
def selected_table2():
    text = request.form.get('textbox')

    return render_template('image.html', label=text)

# 이미지 업로드
@app.route('/upload_image', methods=['POST'])
def upload_image_file():
    if request.method == 'POST':
        # file 객체는 save 함수를 가짐
        file = request.files['uploaded_image']
        if not file: return render_template('image.html', label="No Files")
        label = file.filename
        # 특정 경로에 file명과 같이 저장
        file.save('static/'+label)
        # 파일명은 label로 넘김
        return render_template('image.html', label=label)








@app.route('/about')
def about():
    return 'About Project' #render_template('about.html')

if __name__ == '__main__':
    app.run()