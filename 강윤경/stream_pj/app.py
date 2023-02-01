import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html

import pandas as pd
import numpy as np
import os, sys
from PIL import Image

import plotly.express as px


# 함수


def img_input(subject):
    image_file = st.file_uploader(f'분류할 {subject} 사진을 선택하세요.', type=['png', 'jpg', 'jpeg'])
    if st.button('사진 업로드'):
        img_save('image_files', image_file)
    if st.button('사진 분류하기'):
        if 'img_path' in st.session_state:
            img = Image.open(st.session_state['img_path'])
            st.image(img)
        else:
            st.error('사진을 업로드 해주세요.')
        

def img_save(directory, file):
    # directory 확인, 없으면 생성
    if not os.path.exists(directory):
        os.makedirs(directory)
    if file:
        # 파일 저장
        with open(os.path.join(directory, file.name), 'wb') as f:
            f.write(file.getbuffer())
        img_name = file.name
        st.success('사진 {}이 업로드 되었습니다.'.format(img_name))        
        st.session_state['img_name'] = img_name
        st.session_state['img_path'] = f'./{directory}/{img_name}'
        # 이미지 열기
        # img = Image.open(st.session_state['img_path'])
        # st.image(img)
    else:
        st.error('사진이 선택되지 않았습니다.')

def button_in_button():
    button1 = st.button('Check 1')

    if st.session_state.get('button') != True:

        st.session_state['button'] = button1

    if st.session_state['button'] == True:

        st.write("button1 is True")

        if st.button('Check 2'):

            st.write("Hello, it's working")

            st.session_state['button'] = False

            st.checkbox('Reload')


# 사이드바 : 서비스 목록


task_list = ['경구약제 사진 분류', '꿀벌 사진 분류', '코로나 데이터 분석', '두피 데이터 분석', '심리 상담 챗봇', '당뇨 예측']
icon_list = ['bag-plus', 'bug', 'shield-exclamation', 'clipboard-data', 'chat-dots', 'activity']

with st.sidebar:
    choose = option_menu('인공지능 서비스',
                         task_list,
                         icons=icon_list,
                         menu_icon = 'virus', default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )
st.title(choose)
# selected_task = st.sidebar.selectbox(label='이용할 서비스를 선택하세요.', options=task_list)
# '선택 된 서비스 : ', selected_task


# 메인페이지


if choose == '경구약제 사진 분류':
    img = img_input('의약품')


    # https://blog.naver.com/PostView.nhn?blogId=ys10mjh&logNo=222328257839&parentCategoryNo=&categoryNo=29&viewDate=&isShowPopularPosts=true&from=search
    GDRIVE_HOME = 'content/drive/MyDrive'
    research_root = os.path.join(GDRIVE_HOME, 'research')
    sys.path.append(research_root)


if choose == '꿀벌 사진 분류':
    img_input('꿀벌')



if choose == '코로나 데이터 분석':
    st.error('추후 업데이트 예정입니다.')

if choose == '두피 데이터 분석':
    st.error('추후 업데이트 예정입니다.')

if choose == '심리 상담 챗봇':
    st.error('추후 업데이트 예정입니다.')

if choose == '당뇨 예측':
    st.error('추후 업데이트 예정입니다.')