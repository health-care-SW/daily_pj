from flask import Flask, render_template, request, redirect
import sqlite3
import pandas as pd
# from flask_ngrok import run_with_ngrok  #port를 우회해서 접속가능한 도메인 할당
import os
from models import db
from models import Fcuser
from PIL import Image
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# run_with_ngrok(app)


#----------------------------------------------------------------------

'''
데이터베이스
'''
def get_db(db_name):
    return sqlite3.connect(db_name)


def exe_sql(conn, command:str):
    try:
        conn.execute(command)
        conn.commit()

        if command.split(" ")[0].lower() == 'select':
            df = pd.read_sql(command, conn, index_col = None)
            df_html = df.to_html()
            return df_html, 1
        else:
            return None, 1
    except:
        return None, 0

#---------------------------------------------------------------------

'''
이미지 처리 함수
'''
def image_resize(image, width, height):
        return image.resize((int(width), int(height)))

def image_rotate(image):
    return image.transpose(Image.ROTATE_180)

def image_change_bw(image):
    return image.convert('L')

#-------------------------------------------------------------------

@app.route('/')
def hello_world():
    return "기본 페이지입니다."

# @app.route('/command', methods =['POST'])
# def command():
#    return "TEST" + request.form.get('first_test')

#--------------------------------------------------------------------------------
'''
데이터
'''

@app.route('/data')
def data_page():
    return render_template('data.html')

@app.route('/dbsql', methods=["POST"])
def sql_test():
    if request.method=='POST':
        db_name = request.form.get('db_name')
        sql_command = request.form.get('sql')

        conn = get_db(db_name)

        output, status = exe_sql(conn, sql_command)
        if status == 1:
            #잘 처리됨
            return render_template('data.html', label = "정상 작동") + output            
        else:
            return render_template('data.html', label = "오류 발생", output = None)
    else:
        return render_template('data.html')
        
#--------------------------------------------------------------------------------
'''
이미지
'''
@app.route("/index")
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
        img.save(f'static/{file.filename}')

        if is_rotate_180 == 'on':
            img = image_rotate(img)

        if is_change_bw == 'on':
            img = image_change_bw(img)

        if is_change_size == 'on':
            img = image_resize(img, request.form.get('changed_width'), request.form.get('changed_height'))

        img.save(f'static/changed_{file.filename}')

        # src_dir = os.path.dirname(os.path.abspath(__file__))
        # image_path = os.path.join(src_dir, 'result_image.png')

        # 결과 리턴
        return render_template('index.html', label=file.filename)

#--------------------------------------------------------------------------------
'''
게시판
'''
@app.route('/board')
def board():
    return render_template('bulletinboard.html')


#--------------------------------------------------------------------------------------
'''
로그인
'''

@app.route('/login', methods = ["POST", "GET"])
def login():
    if request.method == 'POST':
        id = request.form['id']
        return f"ID is {id}"
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        #회원정보 생성
        userid = request.form.get('userid') 
        username = request.form.get('username')
        password = request.form.get('password')
        re_password = request.form.get('re_password')
        print(password) # 들어오나 확인해볼 수 있다. 


        if not (userid and username and password and re_password) :
            return "모두 입력해주세요"
        elif password != re_password:
            return "비밀번호를 확인해주세요"
        else: #모두 입력이 정상적으로 되었다면 밑에명령실행(DB에 입력됨)
            fcuser = Fcuser()         
            fcuser.password = password           #models의 FCuser 클래스를 이용해 db에 입력한다.
            fcuser.userid = userid
            fcuser.username = username      
            db.session.add(fcuser)
            db.session.commit()
            return "회원가입 완료"
        return redirect('/')
        

#--------------------------------------------------------------------------------
if __name__ == "__main__":
    basedir = os.path.abspath(os.path.dirname(__file__))  # database 경로를 절대경로로 설정함
    dbfile = os.path.join(basedir, 'db.sqlite') # 데이터베이스 이름과 경로
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True     # 사용자에게 원하는 정보를 전달완료했을때가 TEARDOWN, 그 순간마다 COMMIT을 하도록 한다.라는 설정
    #여러가지 쌓아져있던 동작들을 Commit을 해주어야 데이터베이스에 반영됨. 이러한 단위들은 트렌젝션이라고함.
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   # True하면 warrnig메시지 유발, 

    db.init_app(app) #초기화 후 db.app에 app으로 명시적으로 넣어줌
    db.app = app
    db.create_all()   # 이 명령이 있어야 생성됨. DB가


    app.run(host='127.0.0.1', port=5000, debug=True) 

    