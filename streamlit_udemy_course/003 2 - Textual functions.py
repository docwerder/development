import streamlit as st 
import pandas as pd
# Text 

st.text("Hey this is a text")

a = "sreeram"

st.text("this is {}".format(a))

# Header

st.header("This is a header")

# Sub header

st.subheader("This is a subheader")

# Title

st.title("This is a Title")

# Markdown

st.markdown("This is a markdown")

# Bootstrap Text

st.success("Hurray")
st.warning("This is a warning")
st.info("This is an advice")
st.error("You made a mistake")

# write - The Superior

st.write("You are on earth")

st.write(300*3) # Performing Mathematical Operations

# Using write() to Create a dataframe

st.write(pd.DataFrame({"Name": ["Adith", "Sreeram"], 
"age":[17,18]}))