from flask import Flask, render_template, request
import os
from PIL import Image

# flask는 html 파일을 template 폴더 안에서, 나머지 js, css, image 파일 등은 static 폴더 안에서 참조를 한다. 
# 기본적으로 template 폴더와 static폴더는 content/template, content/static로 경로 설정이 되어있는데 부득이하게 그러한 경로설정이 불가능할 경우 임의로 폴더 경로설정을 해줄 수 있다.

app = Flask(__name__)

''' 이미지 처리 함수 '''
def image_resize(image, width, height):
    return image.resize((int(width), int(height)))

def image_rotate(image):
    return image.transpose(Image.ROTATE_180)

def image_change_bw(image):
    return image.convert('L')

''' 플라스크 '''
@app.route("/index")
def index():
    return render_template('image.html')

@app.route("/image_preprocess", methods=['POST'])
def preprocessing():
    if request.method == 'POST':
        file = request.files['uploaded_image']
        if not file:
            return render_template('index.html', label="No Files")

        img = Image.open(file)

        is_rotate_180 = request.form.get('pre_toggle_0')
        is_change_bw = request.form.get('pre_toggle_1')
        is_change_size = request.form.get('pre_toggle_2')

        if is_rotate_180 == 'on':
            img = image_rotate(img)
        if is_change_bw == 'on':
            img = image_change_bw(img)
        if is_change_size == 'on':
            img = image_resize(img, request.form.get('change_width'), request.form.get('changed_height'))

        img.save('result_image.png')

        src_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(src_dir, 'result_image.png')

        # 결과 리턴
        return render_template('image.html', label=image_path)

@app.route('/upload_image', methods=['POST'])
def upload_image_file():
    if request.method == 'POST':
        file = request.files['upload_image']
        if not file:
            return render_template('image.html', label="No Files")
        label = file
        file.save('static/' + file.filename)
        return render_template('image.html', label=label)
            
if __name__ == '__main__':
    app.run()