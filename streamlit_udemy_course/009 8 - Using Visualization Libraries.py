# packages

import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns
import plotly.express as px

def main():
	st.title("Visualiztion Plots using streamlit")

	df = pd.read_csv("tips.csv")

	st.dataframe(df)

	# using pyplot function

	fig = plt.figure()
	df["sex"].value_counts().plot(kind = "bar")
	st.pyplot(fig)

	fig1 = plt.figure()
	df["total_bill"].value_counts().plot(kind = "kde")
	st.pyplot(fig1)


	fig2 = plt.figure()
	sns.countplot(df["smoker"])
	st.pyplot(fig2)

	fig3 = plt.figure()
	sns.barplot(x = "day", y = "tip", data = df, palette = "summer")
	st.pyplot(fig3)

	# Using streamlit's inbuilt function
	st.bar_chart(df["size"])

	st.bar_chart(df[["total_bill", "tip"]])

	lang = pd.read_csv("lang_data.csv")
	st.dataframe(lang.head())

	list = lang.columns.tolist()
	choice = st.multiselect("Choose Language", list, default = "Python")

	data = lang[choice]
	st.line_chart(data)

	st.area_chart(data)

	# Using Plotly

	a = [1400, 600, 300, 300, 400]

	b = ["House Rent", "Food", "Internet", "Car", "Others"]

	fig4 = px.pie(values = a, names = b, title = "Total Expenses")

	st.plotly_chart(fig4)

	fig5 = px.bar(x = b, y = a)

	st.plotly_chart(fig5)


main()