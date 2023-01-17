from flask import Flask, render_template, request
from flask import Blueprint
import os
from PIL import Image

app = Blueprint("image",__name__, url_prefix="/app_image")

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
@app.route("/")
def index():
    return render_template('image.html')

@app.route('/image_preprocess', methods=['POST'])
def preprocessing():
    if request.method == 'POST':
        img_name = request.form['label1']

        img = Image.open('main/static/'+img_name)

        is_rotate_180 = request.form.get('pre_toggle_0')
        is_change_bw = request.form.get('pre_toggle_1')
        is_change_size = request.form.get('pre_toggle_2')

        if is_rotate_180 == 'on':
            img = image_rotate(img)

        if is_change_bw == 'on':
            img = image_change_bw(img)

        if is_change_size == 'on':
            img = image_resize(img, request.form.get('changed_width'), request.form.get('changed_height'))

        img.save('main/static/images/changed/'+img_name.split('/')[1])
        image_path = 'images/changed/'+img_name.split('/')[1]

        # 결과 리턴
        return render_template('image.html', label= img_name, labeling=image_path)

@app.route('/upload_image', methods=['POST'])
def upload_image_file():
    if request.method == 'POST':
        file = request.files['uploaded_image']
        if not file: return render_template('image.html', label='no file')
        label = file.filename
        file.save('main/static/images/' + file.filename)
    return render_template('image.html', label='images/'+label)