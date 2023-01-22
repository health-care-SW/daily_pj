from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup/', methods=('GET', 'POST'))
def signup(): 
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():

        # username으로 데이터를 조회해서
        user = User.query.filter_by(username=form.username.data).first()

        # 이미 등록된 사용자인지 확인
        if not user:
            user = User(username=form.username.data,
                        # 암호화 저장
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.') # 이미 등록된 경우
    return render_template('auth/signup.html', form=form)    


@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."

        # password와 check_password_hash 함수를 사용하여 입력 비밀번호와 DB 비밀번호 비교
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:

            # 플라스크 세션에 사용자 정보를 저장
            session.clear()
            session['user_id'] = user.id # 세션 키에 user_id 문자열을 저장하고 db id를 저장
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))        