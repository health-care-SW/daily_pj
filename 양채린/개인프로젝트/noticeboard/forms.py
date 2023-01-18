from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
# from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class QuestionForm(FlaskForm):
    # subject = StringField('제품명', validators=[DataRequired('제목은 필수입력 항목입니다.')])
    # content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])
    entpName = StringField('업체명')
    itemName = StringField('제품명')
    efcyQesitm = StringField('효능')
    useMethodQesitm = StringField('사용법')
    atpnQesitm = StringField('주의사항')
    depositMethodQesitm = StringField('보관법')

class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])


class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    # email = EmailField('이메일', [DataRequired(), Email()])
    email = StringField('이메일', [DataRequired()])

class UserLoginForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])


class CommentForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired()])
