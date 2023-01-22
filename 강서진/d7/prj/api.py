from flask import redirect, render_template, request, jsonify, Blueprint, session, g, url_for
from models import User, Post, db
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
    guest = "GUEST"
    return render_template("base.html", guest=guest)


# 회원가입 페이지
@board.route("/join", methods=["GET", "POST"])
def join():
    guest = "GUEST"
    # 세션 x 로그인 x (아예 첫 구동)
    if 'login' not in session:        
        # 가입 폼 제출시 ("POST")
        if request.method=="POST":
            # join 사이트에서 username, user_pw 받아옴
            username = request.form['username']
            user_pw = request.form['user_pw']
            user_email = request.form['user_email']
            pw_hash = bcrypt.generate_password_hash(user_pw)

            new_user = User(username, user_pw, user_email, pw_hash)
            # db 에 user 추가
            db.session.add(new_user)
            db.session.commit()

            return render_template('login.html', message="You're now registered.", guest=guest)
               
        # 가입 페이지로 이동 ("GET")
        else:
            return render_template('join.html', guest=guest)
        
    else:
        # 세션 o 로그인 o
        if session['login'] is not None:
            return render_template('base.html', message="You're already one of us!")

        # 세션 o 로그인 x
        else:
            # 가입 폼 제출시 ("POST")
            if request.method=="POST":
                # join 사이트에서 username, user_pw 받아옴
                username = request.form['username']
                user_pw = request.form['user_pw']
                user_email = request.form['user_email']
                pw_hash = bcrypt.generate_password_hash(user_pw)

                new_user = User(username, user_pw, user_email, pw_hash)
                # db 에 user 추가
                db.session.add(new_user)
                db.session.commit()

                return render_template('login.html', message="You're now registered.", guest=guest)
                
            # 가입 페이지로 이동 ("GET")
            else:
                return render_template('join.html', guest=guest)
        

@board.route('/login', methods=["GET","POST"])
def login():
    guest = "GUEST"
    # 세션 x 로그인 x (아예 첫 구동)
    if 'login' not in session:
        # 폼 제출 시 ("POST")
        if request.method=='POST':
            user_email = request.form['user_email']
            user_pw = request.form['user_pw']

            # user_email을 테이블에서 검색해서 가장 첫 데이터를 리밋으로 설정해 가져옴
            user = User.query.filter(User.user_email == user_email).first()

            if user is not None:
                if bcrypt.check_password_hash(user.pw_hash, user_pw):
                    session['login'] = user.username
                    print('login success')
                    print(session['login'])
                    return render_template('profile.html')

                else:
                    print('login fail1-wrong pw')
                    return render_template('login.html', message = "Wrong password! Try again.", guest=guest)
                    
            else:
                print('login fail2-user is None')               
                return render_template('login.html', message = "Unregistered email! Register first.", guest=guest)

        # 링크로 접근 ("GET")
        else:
            return render_template('login.html', guest=guest)           

    else:
        # 세션 o 로그인 o
        if session['login'] is not None:
            return render_template('base.html', message="You're already logged in.")

        # 세션 o 로그인 x
        else:        
            # 폼 제출 시 ("POST")
            if request.method=='POST':
                user_email = request.form['user_email']
                user_pw = request.form['user_pw']

                user = User.query.filter(User.user_email == user_email).first()

                if user is not None:
                    if bcrypt.check_password_hash(user.pw_hash, user_pw):
                        session['login'] = user.username
                        print('login success')
                        print(session['login'])
                        return render_template('profile.html')

                    else:
                        print('login fail1-wrong pw')
                        return render_template('login.html', message = "Wrong password! Try again.")
                        
                else:
                    print('login fail2-user is None')                    
                    return render_template('login.html', message = "Unregistered email! Register first.")

            # 링크로 접근 ("GET") 
            else:
                return render_template('login.html')


# profile 이동 시 url에 해당 계정의 username이 나오게 하는 법?
# @board.route("/profile/<username>/", methods=["GET"])
# def profile(username):
#     username = session['login']
#     return render_template("profile.html", username=username)

@board.route('/profile')
def profile():
    guest = "GUEST"
    # 세션 x 로그인 x
    if 'login' not in session:
        return render_template('login.html', message="Log in to see your profile.", guest=guest)

    # 세션 o
    else:
        # 세션 o 로그인 x
        if session['login'] is None:
            return render_template('login.html', message="Log in to see your profile.", guest=guest)

        # 세션 o 로그인 o
        else:
            post_by_u = Post.query.filter(Post.author == session['login'])
            return render_template('profile.html', post_by_u=post_by_u)

@board.route("/logout")
def logout():
    guest = "GUEST"
    if session['login'] is not None:
        session['login'] = None
        return redirect("/") 
    else:
        return render_template("base.html", message="You have to be logged in to log out!", guest=guest)
