from flask import render_template, Blueprint

bp = Blueprint('dtb', __name__, url_prefix='/dtb')


@bp.route('/')
def dtb():
    return render_template('dtb/dtb.html')


