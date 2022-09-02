import pandas as pd 
import streamlit as st 

df = pd.read_csv("tips.csv")

# Method 1

#st.dataframe(df, 500, 500)
st.dataframe(df.style.highlight_max(axis = 0))

# Method 2

#st.table(df)

# Method 3

st.write(df.head())

# Displaying Code Snippet

code = """for i in range(2,11,2):
   print(i)
"""

st.code(code, language = "python")