import streamlit as st
import pandas as pd
import plotly.express as px 
from PIL import Image
from keras.models import load_model
from streamlit_cropper import st_cropper
# from bs4 import BeautifulSoup as bs
from selenium import webdriver
import cv2
import numpy as np
import os
import copy
# import requests

target_pill = ['뉴에르도테캡슐', '듀카브정30/10밀리그램', '듀카브정30/5밀리그램', '라노펜세미정', '락토엔큐캡슐(바실루스리케니포르미스균)\xa0', '루키오정10밀리그램(몬테루카스트나트륨)', '리셀톤캡슐 6.0mg', '리프레가캡슐 75mg', '뮤코원캡슐(에르도스테인)', '바실리포미스캡슐', '베아로탄정 50mg', '베아투스정', '비오메틱스캡슐(바실루스리케니포르미스균)', '비우미정 500mg/병', '아나그레캡슐 0.5mg', '앤도민300프리미엄연질캡슐 300mg/PTP', '에피나레정', '엘도민캡슐 300mg', '엘도스인캡슐(에르도스테인)', '크라틴정 10mg', '크라틴정 20mg', '크라틴정 5mg', '티아프란정', '피타로틴정 2mg']
# 약학정보원 약 코드
drug_cd = ['2016052400013','2016053100044','2016053100043','2016051800012','2016051300001','2016053100033','2016052500022','2016052500003','2016051700009','2016051000018','2016053100001','2016053100005','2016051000004','2016051800001','2016051300003','2016051800004','2016050900002','2016051700013','2016051800009','2016051100002','2016051100001','2016051100003','2016050900008','2016053100020']

def header():
    st.title("경구약제 이미지 분류")

    st.markdown('''
        이전 AI 개인 프로젝트에서 했던 경구약제 이미지 분류입니다.  
        다음과 같은 약제종류에서만 가능합니다.
    ''')
    df = pd.DataFrame(target_pill)
    df.columns = ["이름"]
    st.table(df)

def upload_file(directory, file):
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(os.path.join(directory, file.name), 'wb') as f:
        f.write(file.getbuffer())
    return st.success('업로드 완료: {} in {}'.format(file.name, directory))

def crop_image():
    image = st.file_uploader('약제 이미지를 업로드 해주세요', type=['png'])
    if image != None:
        upload_file('images', image)
        img = Image.open(image)
        st.write("Drag the crop box")
        cropped_img = st_cropper(img, realtime_update=True, box_color='#FFFFFF')
        print(type(cropped_img))
        st.write("Preview")
        return cropped_img
    else:
        st.text("이미지가 아직 업로드 되지 않았습니다.")

def flip_TB(img):
    global cropped
    cropped = img.transpose(Image.FLIP_TOP_BOTTOM)
    return cropped

def flip_LR(img):
    global cropped
    cropped = img.transpose(Image.FLIP_LEFT_RIGHT)
    return cropped

def classification(image):
    img = image.convert("RGB")
    arr_img = [cv2.resize(np.array(img), (64,64))]
    arr_img = [i/255.0 for i in arr_img]
    model = load_model("/app/daily_pj/김민종/project_streamlit/pill.h5") 
    predicts = model.predict(np.array(arr_img))
    m = max(predicts[0])
    max_idx = list(predicts[0]).index(m)
    predict_max_percent = max(predicts[0]) * 100
    predict = predicts
    return max_idx, predict_max_percent, predict

def pill_info(idx):
    # info = requests.get("https://www.health.kr/searchDrug/result_drug.asp?drug_cd=%s"%(drug_cd[int(idx)]))
    # soup = bs(info.text, "html.parser")
    # title = soup.select('#result_drug_name')
    # company = soup.select('#upso_title')
    # print(title)
    # print(company)
    # html = soup.select("td")
    # print(html) 
    # st.markdown(html, unsafe_allow_html= True)
    driver = webdriver.Chrome()
    driver.get("https://www.health.kr/searchDrug/result_drug.asp?drug_cd=%s"%(drug_cd[int(idx)]))


def disable(b):
    st.session_state["disabled"] = b

if __name__ == "__main__":
    header()
    cropped = crop_image()
    img = copy.deepcopy(cropped)

    if cropped != None:
        st.image(img)

        submitted = st.button("submit")
        if submitted:
            max_idx, predict_max_percent, predict = classification(cropped)
            st.write(target_pill[max_idx])
            st.write(f'{predict_max_percent}%')
            st.write(predict)
            # print(max_idx)
            # pill_info(max_idx)