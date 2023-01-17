from flask import Flask, render_template, request, g, redirect, url_for
import os
from PIL import Image

from __main__ import app

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
@app.route("/image")
def image():
    #로그인하지 않았다면 메인페이지
    if g.user == None:
        return redirect(url_for("hello"))

    return render_template('image.html')

@app.route('/image_preprocess', methods=['POST'])
def preprocessing():
    if request.method == 'POST':

        html_img_path = "/static/images"
        img_path = "./static/images"
        #file = request.files['uploaded_image']
        img_name = "/sekiro.png"
        file = img_path + img_name
        if not file: return render_template('index.html', label="No Files")

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

        img.save(img_path + '/result_image.png')

        # src_dir = os.path.dirname(os.path.abspath(__file__))
        # image_path = os.path.join(src_dir, '../static/images/sekiro.png')

        # 결과 리턴
        return render_template('image.html', srcImg = html_img_path + '/sekiro.png', resultImg =html_img_path + '/result_image.png')

if __name__ == '__main__':
    app.run(debug=True)
