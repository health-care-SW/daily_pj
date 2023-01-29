import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Avocado Prices dashboard")

st.markdown('''
테스트용 데시보드를 만들어봅시다
''')

avocado = pd.read_csv("avocado.csv")

table = avocado.groupby("type")[['total_volume', 'average_price']].mean()

st.dataframe(table)

selected_geo = st.selectbox(label="Geography", options=avocado['geography'].unique())
submitted = st.button("submit")

if submitted:
    line_fig = px.line(
        avocado[avocado['geography'] == selected_geo],
        x='date', y='average_price',
        color='type',
        title='test'
    )
    st.plotly_chart(line_fig)


#stream.io 기능 구현
number = st.slider("Pick a number", 0, 100)
date = st.date_input("Pick a date")

