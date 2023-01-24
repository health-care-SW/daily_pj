from flask import render_template, request, redirect, url_for, Blueprint, session, g
from model import User
from PIL import Image
from keras.models import load_model
import cv2
import numpy as np

classi = Blueprint('classification',__name__)
target_pill = ['뉴에르도테캡슐', '듀카브정30/10밀리그램', '듀카브정30/5밀리그램', '라노펜세미정', '락토엔큐캡슐(바실루스리케니포르미스균)\xa0', '루키오정10밀리그램(몬테루카스트나트륨)', '리셀톤캡슐 6.0mg', '리프레가캡슐 75mg', '뮤코원캡슐(에르도스테인)', '바실리포미스캡슐', '베아로탄정 50mg', '베아투스정', '비오메틱스캡슐(바실루스리케니포르미스균)', '비우미정 500mg/병', '아나그레캡슐 0.5mg', '앤도민300프리미엄연질캡슐 300mg/PTP', '에피나레정', '엘도민캡슐 300mg', '엘도스인캡슐(에르도스테인)', '크라틴정 10mg', '크라틴정 20mg', '크라틴정 5mg', '티아프란정', '피타로틴정 2mg']

'''
이미지 처리 함수
'''
# 처리 옵션
def image_resize(image, width, height):
        return image.resize((int(width), int(height)))

def image_rotate(image):
    return image.transpose(Image.ROTATE_180)


@classi.before_app_request
def load_logged_in_user():
    user_id = session.get('login')
    if user_id is None:
        g.user = None
    else:
        g.user = User.find(user_id)


@classi.route("/image_preprocess", methods=['GET','POST'])
def preprocessing():
    if request.method == 'POST':
        # 폼에서 전달 받은 이미지 가져옴
        file = request.files['uploaded_image']
        # 원본이미지 해당 경로에 저장
        file.save('./static/assets/images/original.png')
        # 가져온게 없으면 다시 index로 
        if not file: return render_template('main.html', label="No Files")

        # 이미지 변수 
        img = Image.open(file)

        # 체크박스 상태 확인
        is_rotate_180 = request.form.get('pre_toggle_0')
        is_change_size = request.form.get('pre_toggle_2')

        # 체크박스 처리 (체크인지 아닌지 "on"이면 이미지 처리 진행)
        if is_rotate_180 == 'on':
            img = image_rotate(img)

        if is_change_size == 'on':
            img = image_resize(img, request.form.get('changed_width'), request.form.get('changed_height'))
        # 수정 이미지 해당 경로에 저장
        img.save('./static/assets/images/fix.png')

        # 결과 리턴
        return redirect(url_for("classification.classification"),code=307)
    else:
        return redirect(url_for("board.main", error=1))

@classi.route("/classification", methods=["GET","POST"])
def classification():
    if request.method == 'POST':
        img = Image.open("./static/assets/images/fix.png").convert("RGB")
        arr_img = [cv2.resize(np.array(img), (64,64))]
        arr_img = [i/255.0 for i in arr_img]
        model = load_model("./static/assets/model/pill.h5") 
        predicts = model.predict(np.array(arr_img))
        m = max(predicts[0])
        max_idx = list(predicts[0]).index(m)
        predict_max_percent = max(predicts[0]) * 100
        predict = predicts
        return redirect(url_for('classification.result', pre = predict, idx=max_idx, percent=predict_max_percent))
    else:
        return redirect(url_for("board.main", error=1))


@classi.route("/result",methods=["POST","GET"])
def deny_result():
    if request.method == 'POST' or request.method == 'GET':
        return redirect(url_for("board.main",error=1))


@classi.route("/result/<pre>&<idx>&<percent>",methods=["POST","GET"])
def result(pre,idx,percent):
    if request.method == 'POST' or request.method == 'GET':
        return render_template("result.html",pill_name=target_pill[int(idx)], percent=percent)
