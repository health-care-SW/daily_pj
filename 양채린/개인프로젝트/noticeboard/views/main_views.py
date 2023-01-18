from flask import Blueprint, url_for
from werkzeug.utils import redirect
from models import Answer
from data import initial_insert
from models import User

bp = Blueprint('main', __name__, url_prefix='/')

flag = False

@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'


@bp.route('/')
def index():
    user = User.query.filter_by(username='admin').first()
    if not user:
        url = 'http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList'
        params ={'serviceKey' : 'kQ4M06xZZQmh7mwbNBpWs2PLjyMWRMVYdQ6EJB26Wxx0zucRb7Oc8zyDrqY1ACCOlGd7c1Oirdx/2cJK/MxsTA==', 'pageNo' : '1', 'numOfRows' : '9', '_returnType' : 'xml' }
        initial_insert(url, params)
        flag = True
    return redirect(url_for('question._list'))


