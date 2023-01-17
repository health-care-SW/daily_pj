from flask import Flask, render_template, request
import os
from PIL import Image
from db_connect import db
from flask_bcrypt import Bcrypt
import pymysql
from api import board

app = Flask(__name__)
app.register_blueprint(board)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://hchang:devpass@127.0.0.1:3306/board"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'ekdwls'

db.init_app(app)
bcrypt = Bcrypt(app)

if __name__ == '__main__':
    app.run(debug=True)

app = Flask(__name__)
app.register_blueprint(board)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://hchang:devpass@127.0.0.1:3306/board"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'ekdwls'

db.init_app(app)
bcrypt = Bcrypt(app)

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
    return render_template('index2.html')

@app.route('/image_preprocess', methods=['POST'])
def preprocessing():
    if request.method == 'POST':
        file = request.files['uploaded_image']
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

        img.save('result_image.png')

        src_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(src_dir, 'result_image.png')

        return render_template('index.html', label=image_path)

if __name__ == '__main__':
    app.run()

