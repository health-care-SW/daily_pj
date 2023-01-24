from flask import Flask, render_template, request
from app_data import data
# from flask_ngrok import run_with_ngrok
import os
from PIL import Image

app = Flask(__name__)
app.register_blueprint(data)
# run_with_ngrok(app)

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
    return render_template('index.html')


@app.route("/image")
def image():
    return render_template('image.html')


@app.route('/image_preprocess', methods=['POST'])
def preprocessing():
    if request.method == 'POST':
        file = request.files['uploaded_image']
        if not file: return render_template('index.html', label="No Files")

        img = Image.open(file)

        is_rotate_180 = request.form.get('pre_toggle_0')
        is_change_bw = request.form.get('pre_toggle_1')
        is_change_size = request.form.get('pre_toggle_2')

        img.save('static/result_image.png')

        if is_rotate_180 == 'on':
            img = image_rotate(img)

        if is_change_bw == 'on':
            img = image_change_bw(img)

        if is_change_size == 'on':
            img = image_resize(img, request.form.get('changed_width'), request.form.get('changed_height'))

        img.save('static/changed_result_image.png')
        image_path='result_image.png'

        # 결과 리턴
        return render_template('image.html', label=image_path)

if __name__ == '__main__':
    app.run()
