from flask import redirect, render_template, request, jsonify, Blueprint, session, g, url_for
from models import User, db
from flask_bcrypt import Bcrypt


board = Blueprint('api', __name__)
bcrypt = Bcrypt()


# 세션에 로그인 기록이 있나 확인는지 사용자를 확인하는 기능
@board.before_app_request
def load_logged_in_user():
    username = session.get('login')
    if username is None:
        g.user = None
    else:
        g.user = db.session.query(User).filter(User.id == username).first()


# base.html이 메인
@board.route("/", methods=['GET', "POST"])
def home():
    return render_template("base.html")


# 회원가입 페이지
@board.route("/join", methods=["GET", "POST"])
def join():
    if request.method=="POST":
        # join 사이트에서 username, user_pw 받아옴
        # print(request.form)
        username = request.form['username']
        user_pw = request.form['user_pw']
        user_email = request.form['user_email']
        pw_hash = bcrypt.generate_password_hash(user_pw)

        new_user = User(username, user_pw, user_email, pw_hash)
        # db 에 user 추가
        db.session.add(new_user)
        db.session.commit()

        return render_template('login.html')
    else:
        return render_template('join.html')


@board.route('/login', methods=["GET","POST"])
def login():
    # 폼 제출 시 
    if request.method=='POST':
        user_email = request.form['user_email']
        user_pw = request.form['user_pw']
        print(user_email, user_pw)

        # user_email을 테이블에서 검색해서 가장 첫 데이터를 리밋으로 설정해 가져옴
        user = User.query.filter(User.user_email == user_email).first()

        if user is not None:
            if bcrypt.check_password_hash(user.pw_hash, user_pw):
                session['login'] = user.username
                print('login success')
                print(session['login'])
                return render_template('profile.html')
                # return jsonify({"result":"success"})

            else:
                print('login fail1-wrong pw')
                return jsonify({"result":"fail"})
                # return render_template('login.html')
                
        else:
            print('login fail2-user is None')
            # return render_template('login.html')
            return jsonify({"result":"fail"})

    # GET으로 접근 시 
    else:
        return render_template('login.html')

@board.route("/logout")
def logout():
    session['login'] = None
    return redirect("/")

@board.route("/post", methods=["GET"])
def post():
    return render_template("index.html")