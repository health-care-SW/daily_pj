from flask import Blueprint, url_for, render_template, request
from werkzeug.utils import redirect
from PIL import Image


bp = Blueprint('image', __name__, url_prefix='/image')


@bp.route("/")
def image():
    return render_template('image/image.html')
