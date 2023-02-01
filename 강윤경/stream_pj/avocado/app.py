import streamlit as st
import pandas as pd

# 시각화 라이브러리. 표 예쁘게
import plotly.express as px

# st.title('Avocado Prices dashboard')

st.markdown('''
# Avocado Prices dashboard
테스트용 대시보드를 만들어봅시다.
Data source : [kaggle](https://www.kaggle.com/datasets/timmate/avocado-prices-2020)
''')

avocado = pd.read_csv('avocado.csv')

# type별로 묶은 값을 평균값
table = avocado.groupby('type').mean()

# 특정 표만 받아 보기
table_tot_av = avocado.groupby('type')['total_volume', 'average_price'].mean()


# 위의 값을 streamlit에 호스팅하기
st.dataframe(table_tot_av)

# geography가 los angeles인 것만 받기
# line_fig = px.line(
#     avocado[avocado['geography'] == 'Los Angeles'],
#     x='date', y='average_price',
#     # 타입에 따라 색을 나누겠다
#     color='type',
#     title='Test dashboard'
#     )

# st.plotly_chart(line_fig)

# selectbox - options : 불러올 내용, label : 실제 띄워줄 내용
selected_geo = st.selectbox(label='Geography', options=avocado['geography'].unique())

submitted = st.button('Submit')

# submit 버튼 눌리면
if submitted:
    line_fig = px.line(
    avocado[avocado['geography'] == selected_geo],
    x='date', y='average_price',
    color='type',
    # title='{} dashboard'.format(selected_geo)
    title=f'{selected_geo} dashboard'

    )

    st.plotly_chart(line_fig)
