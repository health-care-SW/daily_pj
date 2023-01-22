from flask import render_template, request, Blueprint, session
# from flask_ngrok import run_with_ngrok
import os
from PIL import Image



def image_resize(image, width, height):
    return image.resize((int(width), int(height)))

def image_rotate(image):
    return image.transpose(Image.ROTATE_180)

def image_change_bw(image):
    return image.convert('L')

# -------------------------------------------

# bp = Flask(__name__)
# run_with_ngrok(bp)
bp = Blueprint("image", __name__, url_prefix="/img")


@bp.route("/")
def index():
    guest = "GUEST"
    if session['login']:
        return render_template("image.html")
    else:
        return render_template('login.html', message="You need to login first.", guest=guest)


@bp.route("/image_preprocess", methods=["POST"])
def preprocessing():
    if request.method=="POST":
        file=request.files['uploaded_image']
        if not file: 
            return render_template('image.html', label="NO FILES")

        label = file.filename
        file.save('./static/'+label)

        img = Image.open(file)

        is_rotate_180 = request.form.get('pre_toggle_0')
        is_change_bw = request.form.get('pre_toggle_1')
        is_change_size = request.form.get('pre_toggle_2')

        if is_rotate_180 == 'on':
            img = image_rotate(img)

        if is_change_bw == 'on':
            img = image_change_bw(img)

        if is_change_size == 'on':
            input_width = request.form.get('width')
            input_height = request.form.get('height')
            img = image_resize(img, input_width, input_height)

        img.save(f'./static/result_{label}')

        src_dir = os.path.dirname(os.path.abspath(__file__)) 
        print(src_dir)
        image_path = src_dir + f'\\result_{label}'
        # print(image_path)
        image_title = f'{label}'

        return render_template('image.html', label=image_title)  


# about 페이지
# @bp.route('/about')
# def about():
#     return 'About Project'


# if __name__ == '__main__':
#     bp.run()    