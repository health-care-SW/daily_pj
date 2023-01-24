from flask import Blueprint, render_template, request
import os
from PIL import Image

bp = Blueprint('image', __name__, url_prefix='/image')

'''
이미지 처리 함수
'''
def image_resize(image, width, height):
        return image.resize((int(width), int(height)))

def image_rotate(image):
    return image.transpose(Image.ROTATE_180)

def image_change_bw(image):
    return image.convert('L')

'''
플라스크
'''
@bp.route("/")
def index():
    return render_template('index.html')

@bp.route('/upload_image/', methods=['POST'])
def upload_image_file():
    if request.method == 'POST':
        file = request.files['uploaded_image'] # 이미지 받기
        if not file: return render_template('image.html', label="No Files")

        # currentPath = os.getcwd()
        # label = f'{currentPath}/flask_project/static/user_id2.png'

        label = file.filename
        # print(label)
        print(2)
        file.save('flask_project/static/'+label) # 그리고 파일을 서버에 저장한다.
        return render_template('image.html', label = label) # 다시 이미지를 출력하기 위해서 파일을 변수로 준다.

@bp.route('/image_preprocess', methods=['POST'])
def preprocessing():
    if request.method == 'POST':
        file = request.files['uploaded_image']
        label = file.filename
        if not file: return render_template('index.html', label="No Files")

        file.save('flask_project/static/'+label) # 그리고 파일을 서버에 저장한다.
        img = Image.open(file)

        is_rotate_180 = request.form.get('pre_toggle_0')
        is_change_bw = request.form.get('pre_toggle_1')
        is_change_size = request.form.get('pre_toggle_2')

        if is_rotate_180 == 'on':
            img = image_rotate(img)

        if is_change_bw == 'on':
            img = image_change_bw(img)

        if is_change_size == 'on':
            img = image_resize(img, request.form.get('changed_width'), request.form.get('changed_height'))

        img.save('flask_project/static/changed_'+label)

        # 결과 리턴
        return render_template('index.html', label=label)