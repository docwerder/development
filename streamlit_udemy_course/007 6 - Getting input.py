import streamlit as st 

# Recieving Input

# text_input

fn = st.text_input("Enter your First Name", max_chars = 10)

password = st.text_input("Enter your Password", type = "password")

#text area

msg = st.text_area("Give your feedback")
st.write(msg)

# number inpts

st.number_input("Enter your age", 5, 50)

# date

st.date_input("When is your next flight")

# time

st.time_input("When is your class time")