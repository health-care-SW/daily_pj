import streamlit as st

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