from flask import Flask, Blueprint, render_template, url_for, session, request, redirect, flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from pybo.models import Question, User
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.connect_db import db
from datetime import datetime

import config
#      print(db_name)
#      return sqlite3.connect(db_name)

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return render_template('home.html')
    # question_list = Question.query.order_by(Question.create_date.desc())
    # return render_template('question/question_list.html', question_list=question_list)


@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question)

#회원가입  
@bp.route('/register', methods=['GET','POST'])
def register():
    
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        )
            db.session.add(user)
            db.session.commit()
            return render_template('login/login_form.html')
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('login/register.html', form=form)
        # id = request.form.get('id')
        # passwd = request.form.get('pwd')
        

        # con = get_db('./' + 'test_')
        # cursor = con.cursor()
        # sql = "select id, username, passwd from user where id = " + "'" + id + "'" 
        # cursor.execute(sql)
        # rows = cursor.fetchall()
        # for rs in rows:
        #     if id == rs[0] and passwd == rs[2]:
        #         session['id'] = id
        #         sql2 = "select * from board order by timestamp desc"
        #         cursor.execute(sql2)
        #         rows2 = cursor.fetchall()
        #         lists = rows2
        #         return render_template('login/login_form.html')
        #     else:
        #         return redirect('login/login_form.html')
        


@bp.route('/login', methods=['GET','POST'])
def login():

    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            # question_list = Question.query.order_by(Question.create_date.desc())
    
            # return render_template('question/question_list.html', question_list=question_list)
            return render_template('home.html')
        flash(error)
    return render_template('login/login_form.html', form=form)

@bp.route('/board', methods=['GET','POST'])
def board():
    question_list = Question.query.order_by(Question.create_date.desc())
    
    return render_template('question/question_list.html', question_list=question_list)


@bp.route('/upload',  methods=['GET','POST'])
def upload():
    question = Question()
    
    if request.method == 'POST':

        question = Question(subject=request.form.get('subject'), content=request.form.get('content'), create_date=datetime.now())

        db.session.add(question)
        db.session.commit()
        question_list = Question.query.order_by(Question.create_date.desc())
        return render_template('question/question_list.html', question_list = question_list)

    return render_template('image.html')

    


       


