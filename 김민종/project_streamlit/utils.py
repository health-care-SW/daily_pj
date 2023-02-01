import streamlit as st
from PIL import Image

def flip_TB():
    st.session_state.image = st.session_state.image.transpose(Image.FLIP_TOP_BOTTOM)

def flip_LR():
    st.session_state.image = st.session_state.image.transpose(Image.FLIP_LEFT_RIGHT)

def rotate(option):
    degree = option[:-1]
    if degree == '90':
        st.session_state.image = st.session_state.image.transpose(Image.ROTATE_90)
    elif degree == '180':
        st.session_state.image = st.session_state.image.transpose(Image.ROTATE_180)
    else:
        st.session_state.image = st.session_state.image.transpose(Image.ROTATE_270)