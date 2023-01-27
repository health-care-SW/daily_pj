import streamlit as st

st.set_page_config(
    page_title="MainPage",
    page_icon=":wave:",
)

st.write("# This is main page! :wave:")


st.markdown(
    """
    두 모델을 활용한 두 페이지  
    **👈 Select a page from the sidebar**
    ### 합격예측모델
    - 출처 [Youtube](https://www.youtube.com/watch?v=8ftqlASt6HY)

    ### 챗봇모델
    - 출처 [Hugging Face](https://huggingface.co/byeongal/Ko-DialoGPT)
    """
)
