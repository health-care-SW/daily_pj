from flask import redirect, request, render_template, jsonify, Blueprint, session, g
from pyproject.models import User, Post
from flask_bcrypt import Bcrypt

from pyproject.db_connect import db

# 테스트용
# from flask import Flask
# board = Flask(__name__)

board = Blueprint('board',__name__)
bcrypt = Bcrypt()



'''
요청마다 로그인 판단
'''
# before_app_request : 모든 URI 접근시 실행되는 함수
# @board.before_app_request
@board.before_request
def load_logged_in_user():
    user_id = session.get('login')
    if user_id is None:
        g.user = None
    else:
        g.user = db.session.query(User).filter(User.id == user_id).first()

@board.route("/")
def home():
    return render_template("base.html")

@board.route("/post", methods=["GET"])
def post():
    return render_template("index.html")

@board.route("/join",methods=["GET","POST"])
def join():
    if request.method == 'GET':
        return render_template('join.html')
    else:
        user_id = request.form['user_id']
        user_pw = request.form['user_pw']
        pw_hash = bcrypt.generate_password_hash(user_pw)

        user = User(user_id, pw_hash)
        db.session.add(user)
        db.session.commit()
        return jsonify({"result":"success"})
       

''''
로그인
'''
# 로그인을 위한 login() 함수를 완성하세요.
@board.route("/login",methods=['GET','POST'])
def login():
    # GET이면 login.html 화면
    if request.method == 'GET':
        return render_template("login.html")
    
    # POST면 user_id, user_pw 받아옴
    else:
        user_id = request.form['user_id']
        user_pw = request.form['user_pw']
        # DB에서 사용자 검색, user 변수 저장
        user = User.query.filter(User.user_id == user_id).first()

        # DB에 user 있을 경우
        if user is not None:
            # DBd의 user.user_pw와 user_pw 변수 일치 시,
            if bcrypt.check_password_hash(user.user_pw, user_pw):
                # return true (True 반환)
                # session['login']에 user.id 저장, success 반환
                # session['키값'] = 넣고자 하는 값
                # session.pop("키값", None)
                session['login'] = user.id
                return jsonify({"result":"success"})
            else:
                # 변수 일치하지 않을 시, fail 반환
                return jsonify({"reesult":"fail"})
        else:
            return jsonify({"result":"fail"})

'''
로그아웃
'''
# session['login']을 none으로 지정
@board.route("/logout")
def logout():
    session['login'] = None
    return redirect("/")



# 테스트용
# if __name__ == '__main__':
#     board.run(debug=True)
