from flask import Flask, render_template, request
# from flask_ngrok import run_with_ngrok
import os
from PIL import Image

app = Flask(__name__)
# run_with_ngrok(app)


def image_resize(image, width, height):
    return image.resize((int(width), int(height)))

def image_rotate(image):
    return image.transpose(Image.ROTATE_180)

def image_change_bw(image):
    return image.convert('L')

# -------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/image_preprocess", methods=["POST"])
def preprocessing():
    if request.method=="POST":
        file=request.files['uploaded_image']
        if not file: 
            return render_template('index.html', label="NO FILES")
        label = file.filename # cat.jpg
        file.save('static/'+label)

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
            img = image_resize(img, int(input_width), int(input_height))

        img.save(f'static/result_{label}')

        # src_dir = os.path.dirname(os.path.abspath(__file__)) # C:\Users\Amy\Desktop\2023\flask_prj
        #image_path = os.path.join(src_dir, '/result_image.png') # C:/result_image.png
        image_title = f'{label}'

        return render_template('index.html', label=image_title) 
        # return render_template('result.html', label=image_title) 


# 새 창에 새로운 이미지 띄우고, 다시 index 페이지로 돌아가는 버튼이 있는 창
# @app.route("/back_to_index", methods=["POST"])
# def go_back():
#     return render_template('index.html')


# about 페이지
@app.route('/about')
def about():
    return 'About Project' #render_template('about.html')


if __name__ == '__main__':
    app.run()    
