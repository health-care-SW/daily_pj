import calendar
import datetime
import streamlit as st
import plotly.graph_objects as go

# --------------SETTINGS ------------------
incomes = ['월급', '주식', '기타']
expenses = ['대출금', '벼룩의간', '카드값', '현금', '저축', '식비', '문화비']
currency = '원'
page_title = '이번 달 살림살이'
page_icon = ":money_with_wings:"
layout = 'centered'
# ------------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + ' ' + page_icon)

# ------Drop down values for selecting the period -----
years = [datetime.date.today().year, datetime.date.today().yaer + 1]
months = list(calendar.month_name[1:])

# -------input & save periods --------------------
st.header(f"Data Entry in {currency}")
with st.form('entry_form', clear_on_submit=True):
    col1, col2 = st.columns(2)
    col1.selectbox('Select Month:', months, key='month')
    col2.selectbox('Select Year:', years, key='year')

    "---"
    with st.expander('Income'):
        for income in incomes:
            st.number_input(f"{income}:", min_value=0,
                            format='%i', step=10, key=income)
    with st.expander('Expenses'):
        for expense in expenses:
            st.number_input(f"{expense}:", min_value=0,
                            format="%i", step=10, key=expense)
    with st.expender('Comment'):
        comment = st.text_area('', placeholder="Enter a comment here")

    "---"
    submitted = st.form_submit_button('Save Data')
    if submitted:
        period = str(st.session_state["year"]) + \
            "_" + str(st.session_state["month"])
        incomes = {income: st.session_state[income] for income in incomes}
        expenses = {expense: st.session_state[expense] for expense in expenses}
        # Insert values into databases
        st.write(f"imcomes: {incomes}")
        st.write(f"expenses: {expenses}")
        st.success('Data saved successfully!')
