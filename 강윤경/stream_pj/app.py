import streamlit as st
import pandas as pd
import plotly.express as px
import os
from PIL import Image


st.title('인공지능 서비스')

task_list = ['경구약제 사진 분류', '꿀벌 사진 분류', '코로나 데이터 분석', '두피 데이터 분석', '심리 상담 챗봇', '당뇨 예측']
selected_task = st.sidebar.selectbox(label='이용할 서비스를 선택하세요.', options=task_list)

'선택 된 서비스 : ', selected_task

def save_image(directory, file):
    # directory 확인, 없으면 생성
    if not os.path.exists(directory):
        os.makedirs(directory)
    if file:
        # 파일 저장
        with open(os.path.join(directory, file.name), 'wb') as f:
            f.write(file.getbuffer())
        # 선택된 사진 띄우기
        # img = Image.open(file)
        # st.image(img)
        image_name = file.name
        # st.success('사진 {}이 업로드 되었습니다.'.format(file.name))
        st.success('사진 {}이 업로드 되었습니다.'.format(image_name))
        return image_name

        
    else:
        st.error('사진이 선택되지 않았습니다.')


def image_input(subject):
    image_file = st.file_uploader(f'분류할 {subject} 사진을 선택하세요.', type=['png', 'jpg', 'jpeg'])
    image_upload_bt = st.button('사진 업로드')
    if image_upload_bt:
        img_name = save_image('image_files', image_file)
        return img_name
    

if selected_task == '경구약제 사진 분류':
    img_name = image_input('의약품')
    if img_name:
        img = Image.open(f'./image_files/{img_name}')
        # st.image(img)
        task_start_bt = st.button('사진 분류하기')

# 해결할 것 : task_start 버튼을 눌렀을 때 이전에 image_upload 버튼 눌렀을 때 저장된 값이 사라짐



if selected_task == '꿀벌 사진 분류':
    image_input('꿀벌')

if selected_task == '코로나 데이터 분석':
    st.error('추후 업데이트 예정입니다.')

if selected_task == '두피 데이터 분석':
    st.error('추후 업데이트 예정입니다.')

if selected_task == '심리 상담 챗봇':
    st.error('추후 업데이트 예정입니다.')

if selected_task == '당뇨 예측':
    st.error('추후 업데이트 예정입니다.')
