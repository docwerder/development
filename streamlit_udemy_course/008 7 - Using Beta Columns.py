import streamlit as st 

country = ["USA", "India", "Canada", "UK", "Australia"]
st.selectbox("Country", country)

col1, col2  = st.beta_columns(2)

with col1:
	fname = st.text_input("Enter your first name")

with col2:
	lname = st.text_input("Enter your Last name")


st.text_area("Enter your Address")

city, state, zc = st.beta_columns([4,3,2])

with city:
	c = st.text_input("City")

with state:
	s = st.text_input("State")

with zc:
	z = st.text_input("ZipCode")


mail, pn = st.beta_columns([3,1])

with mail:
	email = st.text_input("Enter your Email")

with pn:
	phone = st.text_input("Enter your Phone Number")


#st.button("Save")
if st.button("Save"):
	st.success("Your Information was saved successfully!!")