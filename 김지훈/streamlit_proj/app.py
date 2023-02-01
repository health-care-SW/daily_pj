import streamlit as st
import pandas as pd
from streamlit_chat import message
import plotly.express as px

import chatbot

st.title("Simple Chatbot")

# st.markdown('''

# 테스트용 대시보드
# Data source: [kaggle](https://www.kaggle.com/datasets/timmate/avocado-prices-2020)
# ''')


# avocado = pd.read_csv("avocado-updated-2020.csv")

# table = avocado.groupby("type")[['total_volume', 'average_price']].mean()

# st.dataframe(table)



# selected_geo = st.selectbox(label = "Geography", options= avocado['geography'].unique())

# submitted = st.button("Submit")

# if submitted:
#     line_fig = px.line(
#     avocado[avocado['geography'] == selected_geo],
#     x = 'date', y = 'average_price',
#     color='type',
#     title = f'{selected_geo} dashboard'
#     )

#     st.plotly_chart(line_fig)
    
def clear_text():
    st.session_state["text"] = ""

#print(st.session_state)


if 'message_history' not in st.session_state:
    st.session_state.message_history = []
    

keyNum = 0
for message_ in st.session_state.message_history:
    if len(message_[0]) != 0:
        message(message_[0], key = "user" + str(keyNum), is_user = True)
    if len(message_[1]) != 0:
        message(message_[1], key = "bot" + str(keyNum))
    keyNum += 1



placeholder = st.empty()
input_ = st.text_input("text", key="text", value = "",
                        placeholder="메세지를 입력하세요",
                        )

#print(input_)


st.button("메세지 비우기", on_click=clear_text)

#print(input_)
output_ = "" if input_ == "" else chatbot.chat(input_)
st.session_state.message_history.append((input_, output_))


with placeholder.container():
    if len(input_) != 0:
        message(st.session_state.message_history[-1][0], is_user=True)
    if len(output_) != 0:
        message(st.session_state.message_history[-1][1])
