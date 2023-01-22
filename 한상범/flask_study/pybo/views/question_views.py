from datetime import datetime

from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect

from .. import db
from pybo.models import Question
from pybo.forms import QuestionForm, AnswerForm

'''
인수 1 블루프린트의 '별칭'으로 url_for 함수에서 사용된다.
인수 2 모듈 명 main_views가 전달
인수 3 라우팅 함수의 애너테이션 URL 암페 기본으로 붙일 URL

-> 원래 hello_pybo는 '/'이니 localhost:5000/으로 입력하는데 
url_p가 '/main'이었다면 localhost:5000[/main]/이다. = 애너테이션 URL의 앞에 /main을 붙여야한다.
'''

bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/list/')
def _list():
    question_list = Question.query.order_by(Question.create_date.desc())
    return render_template('question/question_list.html', question_list = question_list)

@bp.route('/create/', methods = ('GET', 'POST'))
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now())
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)

@bp.route('/detail/<int:question_id>/') # 매개변수 URL 매핑 규칙
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id) # 매개변수로 전달 받은 id의 질문
    return render_template('question/question_detail.html', question = question, form=form)