import streamlit as st
import pandas as pd
import plotly.express as px

st.title("==Avocado Prices==")
st.markdown('''
테스트용 데시보드를 만들어봅시다.
Data source: [kaggle](https://www.kaggle.com/datasets/timmate/avocado-prices-2020)
''')

avocado = pd.read_csv("avocado.csv")
table = avocado.groupby("type")['average_price'].mean()
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
