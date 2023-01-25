import streamlit as st
import pandas as pd
import plotly.express as px 
st.title("Avocado Prices dashboard")

st.markdown('''
    테스트용 대시보드를 만들어봅시다.
    Data source: [kaggle](https://www.kaggle.com/datasets/timmate/avocado-prices-2020)
''')

avocado = pd.read_csv("/app/daily_pj/김민종/project_streamlit/avocado.csv")
avg = avocado.groupby("type")[['total_volume','average_price']].mean()

st.dataframe(avg)

selected = st.selectbox(label="Geography",options=avocado['geography'].unique())
submitted = st.button("submit")
if submitted:
    line_fig = px.line(avocado[avocado['geography']== selected],
    x='date',y='average_price', color='type',title=selected)

    st.plotly_chart(line_fig)
