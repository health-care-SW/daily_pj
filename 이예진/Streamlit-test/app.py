import streamlit as st
import pandas as pd

st.write("Testing Streamlit")

lang = st.radio("Your Favourite Language", ("Python", "C", "Java"))

if lang == "Python":
st.write("You selected Python.")
if lang == "C":
st.write("You Selected C")
if lang == "Java":
st.write("You Selected Java")

city = st.selectbox("How would you like to be contacted?", ("Chennai", "Bangalore", "New Delhi"))
st.write("You selected:", city)

level = st.slider("Select Your Expertise Level?", 1, 10, 6)
st.write("You are at Level:", level)



#표 그리기
df = pd.DataFrame({"one": [1, 2, 3], "two": [4, 5, 6], "three": [7, 8, 9]})
st.write(df)

st.title("Connect to Google Sheets")
gsheet_url = "https://docs.google.com/spreadsheets/d/1ixMrhGV1TPn14_oTyEIFjszuwuwO9xkbsc1WEBJH3N0/edit?usp=sharing"
conn = connect()
rows = conn.execute(f'SELECT * FROM "{gsheet_url}"')
df_gsheet = pd.DataFrame(rows)
st.write(df_gsheet)