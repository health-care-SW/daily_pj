from flask import Flask, render_template, request
import os
from PIL import Image


app = Flask(__name__)

'''
이미지 처리 함수
'''
# 처리 옵션
def image_resize(image, width, height):
        return image.resize((int(width), int(height)))

def image_rotate(image):
    return image.transpose(Image.ROTATE_180)

def image_change_bw(image):
    return image.convert('L')

'''
플라스크
'''
@app.route("/index")
def index():
    return render_template('image.html')


@app.route('/image_preprocess', methods=['POST'])
def preprocessing():
    if request.method == 'POST':

        # 폼에서 전달 받은 이미지 가져옴
        file = request.files['uploaded_image']
        # 원본이미지 해당 경로에 저장
        file.save('./static/assets/images/original.jpg')
        # 가져온게 없으면 다시 index로 
        if not file: return render_template('image.html', label="No Files")

        # 이미지 변수 
        img = Image.open(file)

        # 체크박스 상태 확인
        is_rotate_180 = request.form.get('pre_toggle_0')
        is_change_bw = request.form.get('pre_toggle_1')
        is_change_size = request.form.get('pre_toggle_2')

        # 체크박스 처리 (체크인지 아닌지 "on"이면 이미지 처리 진행)
        if is_rotate_180 == 'on':
            img = image_rotate(img)

        if is_change_bw == 'on':
            img = image_change_bw(img)

        if is_change_size == 'on':
            img = image_resize(img, request.form.get('changed_width'), request.form.get('changed_height'))

        # 수정 후 이미지 저장
        img.save('result_image.png')
        img.save('./static/assets/images/fix.jpg')
        src_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(src_dir, 'result_image.png')

        # 결과 리턴
        return render_template('image.html', label=image_path)

if __name__ == '__main__':
    app.run(debug=True)
