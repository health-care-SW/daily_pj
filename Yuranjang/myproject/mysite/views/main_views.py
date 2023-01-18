from flask import Blueprint, url_for, render_template
from werkzeug.utils import redirect


bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def hello_world():
    return render_template('helloworld.html')


@bp.route('/list')
def index():
    return redirect(url_for('question._list'))


