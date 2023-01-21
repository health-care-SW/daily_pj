from flask import Blueprint, url_for
from werkzeug.utils import redirect

'''
인수 1 블루프린트의 '별칭'으로 url_for 함수에서 사용된다.
인수 2 모듈 명 main_views가 전달
인수 3 라우팅 함수의 애너테이션 URL 암페 기본으로 붙일 URL

-> 원래 hello_pybo는 '/'이니 localhost:5000/으로 입력하는데 
url_p가 '/main'이었다면 localhost:5000[/main]/이다. = 애너테이션 URL의 앞에 /main을 붙여야한다.
'''

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'

@bp.route('/')
def index():
    return redirect(url_for('question._list'))