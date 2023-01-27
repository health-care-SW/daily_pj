import streamlit as st
import pandas as pd
from keras.models import load_model


model = load_model('..\\test_model2.h5')


st.title('합격예측')

st.markdown('''
대학원 합격예측 모델 Model Source: [Youtube](https://www.youtube.com/watch?v=8ftqlASt6HY)
''')

st.caption(':green[다른 사람의 지원정보 미리보기]:sunglasses:')
scores = pd.read_csv(
    "./gpascore1.csv", names=['합격여부(0불합/1합)', '토익', '학점', '분류번호'], skiprows=1)
# pd.options.display.float_format = '{:.1f}'.format

st.dataframe(scores, height=150, use_container_width=True)

with st.form(key='my_form'):
    toeic = st.number_input(
        '토익점수를 입력하세요', min_value=100, max_value=990, value=800, step=5)
    st.write(f'현재 입력 점수는 {toeic}입니다.')

    number = st.number_input(
        '학점을 입력하세요', min_value=2.0, max_value=4.5, value=3.5, step=0.1)
    st.write(f'현재 입력 학점은 {round(number,2)}입니다.')

    option = st.selectbox(
        '희망 대학원의 번호를 입력하세요',
        (1, 2, 3, 4))
    st.write(f'현재 입력 번호는 {option}입니다.')

    tb1 = [1, 2, 3, 4]
    indexname = ['가가대학원', '나나대학원', '다다대학원', '라라대학원']
    tb = pd.DataFrame(tb1, index=indexname, columns=['번호'])

    with st.expander("번호를 모른다면?"):
        st.table(tb)

# 예측
    submitted = st.form_submit_button(label='예측 결과 보기')

    if submitted:
        with st.spinner('계산 중...'):
            preval = model.predict([[toeic, number, option]])
            preval1 = preval[0, 0]
        st.text(f'당신의 합격 확률은 {round(preval1*100,5)}% 입니다.')
