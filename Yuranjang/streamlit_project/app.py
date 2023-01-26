import streamlit as st
import pandas as pd
import plotly.express as px


st.title('Avocado')

st.markdown('''
테스트용 대시보드
Data source: [kaggle](https://www.kaggle.com/datasets/timmate/avocado-prices-2020)
''')

avocado = pd.read_csv("./avocado.csv")

table = avocado.groupby("type")['average_price'].mean()

st.dataframe(table)


st.selectbox(label="", options=avocado['geography'].unique())

selected_geo = st.selectbox(
    label="Geography", options=avocado['geography'].unique())

submitted = st.button("SUBmit")

if submitted:
    line_fig = px.line(
        avocado[avocado['geography'] == selected_geo],
        x='date', y='average_price',
        color='type',
        title='Test'
    )
    st.plotly_chart(line_fig)
