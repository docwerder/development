import streamlit as st
st.header("Widgets")

#Buttons
b = st.button("Save")

if b:
	st.success("Your submission have been saved successfully")


st.button("Save", key = "new-save")


# Radio Buttons

status = st.radio("What is your status?", ("Attended", "Didn't Attend"))

if status == "Attended":
	st.success("Thanks for attending")
else:
	st.error("Attend the next meetinf without fail")


# checkbox

if st.checkbox("Show/hide"):
	st.text("this is the secret don't reveal it!!!!")

# Expander

with st.beta_expander("show me the scret"):
	st.text("this is the secret don't reveal it!!!!")


# Select

lang = ["Python", "R", "GO", "PHP", "HTML", "CSS", "JAVA", "C++", "C"]

c = st.selectbox("Choose your favourite languages", lang)

st.write("You selected {}".format(c))


# Multiple Select box

fav_lang = st.multiselect("Choose your favourite languages", lang, default = "GO")


# Slider

age = st.slider("Enter your Age", 5, 90, step = 5)

langg = st.select_slider("Choose a language", options = lang)