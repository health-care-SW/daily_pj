from flask import Flask, render_template, request, redirect
from models import db
import os
from models import Fcuser
from flask import session 
from flask_wtf.csrf import CSRFProtect
from forms import RegisterForm, LoginForm

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def hello():
    return render_template("hello.html")

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
        print(password)


        if not (userid and username and password and re_password) :
            return "모두 입력해주세요"
        elif password != re_password:
            return "비밀번호를 확인해주세요"
        else:
            fcuser = Fcuser()         
            fcuser.password = password 
            fcuser.userid = userid
            fcuser.username = username      
            db.session.add(fcuser)
            db.session.commit()
            return "회원가입 완료"

        return redirect('/')

@app.route('/login', methods=['GET','POST'])  
def login():  
    form = LoginForm() #로그인 폼 생성
    if form.validate_on_submit(): #유효성 검사
        session['userid'] = form.data.get('userid') #form에서 가져온 userid를 session에 저장    
        return redirect('/') #로그인에 성공하면 홈화면으로 redirect
            
    return render_template('login.html', form=form)

if __name__ == "__main__":
    basedir = os.path.abspath(os.path.dirname(__file__))  # database 경로를 절대경로로 설정
    dbfile = os.path.join(basedir, 'db.sqlite') # 데이터베이스 경로와 이름
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'wcsfeufhwiquehfdx'

    csrf = CSRFProtect()
    csrf.init_app(app)

    db.init_app(app)
    db.app = app
    with app.app_context():
        db.create_all()


    app.run(host='127.0.0.1', port=5000, debug=True) 
