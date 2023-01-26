import streamlit as st
import pandas as pd
from streamlit_chat import message
import plotly.express as px

st.title("Avocado Prices Dashboard")

st.markdown('''

테스트용 대시보드
Data source: [kaggle](https://www.kaggle.com/datasets/timmate/avocado-prices-2020)
''')


avocado = pd.read_csv("avocado-updated-2020.csv")

table = avocado.groupby("type")[['total_volume', 'average_price']].mean()

st.dataframe(table)



selected_geo = st.selectbox(label = "Geography", options= avocado['geography'].unique())

submitted = st.button("Submit")

if submitted:
    line_fig = px.line(
    avocado[avocado['geography'] == selected_geo],
    x = 'date', y = 'average_price',
    color='type',
    title = f'{selected_geo} dashboard'
    )

    st.plotly_chart(line_fig)


message_history = []
placeholder = st.empty()
input_ = st.text_input("you:")
output_ = input_
message_history.append((input_, output_))

with placeholder.container():
    for message_ in message_history:
        if len(output_) != 0:
            message(message_[0], is_user=True)
        if len(output_) != 0:
            message(message_[1])