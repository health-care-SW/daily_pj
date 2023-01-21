from datetime import datetime
from flask import Blueprint, url_for, request, render_template
from werkzeug.utils import redirect

from .. import db
from pybo.forms import AnswerForm
from pybo.models import Question, Answer

bp = Blueprint('answer', __name__, url_prefix='/answer')

@bp.route('/create/<int:question_id>', methods=('POST',))
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    if form.validate_on_submit():
        question = Question.query.get_or_404(question_id) # 매개변수로 전달 받은 id의 질문
        content = request.form['content'] # POST 방식으로 전송된 데이터 항목 중 name 속성이 content인 값
        answer = Answer(question = question, content=content, create_date=datetime.now()) # 답변을 하나 만듬
        question.answer_set.append(answer) # 답변에 답변을 더함
        db.session.commit()
        return redirect(url_for('question.detail', question_id=question_id))

    return render_template('question/question_detail.html', question=question, form=form)