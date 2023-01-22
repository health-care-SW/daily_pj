from flask import Blueprint, url_for, render_template, request
from werkzeug.utils import redirect
from PIL import Image


bp = Blueprint('image', __name__, url_prefix='/image')


def image_resize(img, width, height):
    return img.resize((int(width), int(height)))


def image_rotate(img):
    return img.transpose(Image.ROTATE_180)


def image_change_bw(img):
    return img.convert('L')


@bp.route("/")
def image():
    return render_template('image/image_pro.html')


@bp.route('/image_preprocess/', methods=['POST'])
def preprocessing():
    if request.method == 'POST':
        file = request.files['uploaded_image']
        if not file:
            return render_template('image/image_pro.html', label="No Files")

        img = Image.open(file)

        is_rotate_180 = request.form.get('pre_toggle_0')
        is_change_bw = request.form.get('pre_toggle_1')
        is_change_size = request.form.get('pre_toggle_2')

        img.save(f'mysite/static/{file.filename}')

        if is_rotate_180 == 'on':
            img = image_rotate(img)

        if is_change_bw == 'on':
            img = image_change_bw(img)

        if is_change_size == 'on':
            img = image_resize(img, request.form.get('changed_width'), request.form.get('changed_height'))

        img.save(f'mysite/static/changed_{file.filename}')

        # 결과 리턴
        return render_template('image/image_pro.html', label=file.filename)