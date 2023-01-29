import streamlit as st
import pandas as pd
import plotly.express as px

st.markdown('''
# Avocado Prices dashboard
테스트용 데시보드를 만들어봅시다.
Data source: [kaggle](https://www.kaggle.com/datasets/timmate/avocado-prices-2020)
''')

avocado = pd.read_csv("avocado.csv")

table = avocado.groupby("type")['total_volume', 'average_price'].mean()

st.dataframe(table)

line_fig = px.line(
    avocado[avocado['geography'] == "Los Angeles"],
    x='date',
    y='average_price',
    color='type',
    title='Test dashboard'
)

st.plotly_chart(line_fig)

selected_geo = st.selectbox(
    label="Geography", options=avocado['geography'].unique())

submitted = st.button("Sbumit")

if submitted:
    line_fig = px.line(
        avocado[avocado['geography'] == "Los Angeles"],
        x='date', y='average_price',
        color='type',
        title=f'{selected_geo}Test dashboard'
    )

    st.plotly_chart(line_fig)
