import calendar
import datetime
import streamlit as st  # pip install streamlit
# pip install streamlit-option-menu
from streamlit_option_menu import option_menu
import plotly.graph_objects as go

import database as db  # local import

# --------------SETTINGS ------------------
incomes = ['월급', '주식', '기타']
expenses = ['카뱅전세대출', '벼룩의간', '현대카드', '현금지출', '저축', '식비', '문화비', '메리']
currency = 'KRW'
page_title = '이번 달 살림살이'
page_icon = ":money_with_wings:"
layout = 'centered'  # wide if u want
# ------------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + ' ' + page_icon)

# ------Drop down values for selecting the period -----
years = [datetime.datetime.now().year, datetime.datetime.now().year + 1]
months = list(calendar.month_name[1:])


# ------- database interface  ----- 모든 기간동안의 데이터베이스에서 가져오기
def get_all_periods():
    items = db.fetch_all_periods()
    periods = [item["key"] for item in items]
    return periods


# --- Hide streamlit style ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# ---------- navigation menu  -----------------
selected = option_menu(
    menu_title=None,
    options=["Data Entry", "Data Visualization"],
    icons=["pencil-fill", "bar-chart-fill"],
    orientation="horizontal",
)


# -------input & save periods --------------------
if selected == 'Data Entry':  # nav에서 선택시
    st.header(f"Data Entry in {currency}")
    with st.form('entry_form', clear_on_submit=True):
        col1, col2 = st.columns(2)
        col1.selectbox('Select Year:', years, key='year')
        col2.selectbox('Select Month:', months, key='month')

        "---"
        with st.expander('Income'):
            for income in incomes:
                st.number_input(f"{income}:", min_value=0,
                                format='%i', step=10, key=income)
        with st.expander('Expenses'):
            for expense in expenses:
                st.number_input(f"{expense}:", min_value=0,
                                format="%i", step=10, key=expense)
        with st.expander('Comment'):
            comment = st.text_area('', placeholder="Enter a comment here")

        "---"
        submitted = st.form_submit_button("잘 살았다!(Well Saved)")
        if submitted:
            period = str(st.session_state["year"]) + \
                "_" + str(st.session_state["month"])
            incomes = {income: st.session_state[income] for income in incomes}
            expenses = {
                expense: st.session_state[expense] for expense in expenses}
            # Insert values into databases
            db.insert_period(period, incomes, expenses, comment)
            st.success('Data saved successfully!')

# ---------------plot periods  ---------------
if selected == 'Data Visualization':
    st.header('Data Visualization')
    with st.form('saved_periods'):
        period = st.selectbox("Select Period:", get_all_periods())
        submitted = st.form_submit_button("Plot Period")
        if submitted:
            # TODO : get data from databse
            period_data = db.get_period(period)
            comment = period_data.get("comment")
            expenses = period_data.get("expenses")
            incomes = period_data.get("incomes")

            # Create metrics
            total_income = sum(incomes.values())
            total_expense = sum(expenses.values())
            remaining_budget = total_income - total_expense
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Income", f"{total_income} {currency}")
            col2.metric("Total Expense", f"{total_expense} {currency}")
            col3.metric("Remaining Budget", f"{remaining_budget} {currency}")
            st.text(f"Comment: {comment}")

            # Create sankey chart
            label = list(incomes.keys()) + \
                ["Total Income"] + list(expenses.keys())
            source = list(range(len(incomes))) + [len(incomes)] * len(expenses)
            target = [len(incomes)] * len(incomes) + [label.index(expense)
                                                      for expense in expenses.keys()]
            value = list(incomes.values()) + list(expenses.values())

            # Data to dict, dict to sankey
            link = dict(source=source, target=target, value=value)
            node = dict(label=label, pad=20, thickness=30, color="#E694FF")
            data = go.Sankey(link=link, node=node)

            # Plot it!
            fig = go.Figure(data)
            fig.update_layout(margin=dict(l=0, r=0, t=5, b=5))
            st.plotly_chart(fig, use_container_width=True)
