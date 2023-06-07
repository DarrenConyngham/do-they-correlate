import streamlit as st
import plotly.express as px
import pandas as pd
import statsmodels

st.title("Do They Correlate?")
st.subheader("Do Two World Development Indicators have a relationship?")

# Create a DataFrame
df = pd.read_parquet('WDIData2020.parquet')


# Create a dropdown menu for the x-axis
options = df.columns
x_axis = st.selectbox("Select x-axis", options)

# Create a dropdown menu for the y-axis
y_axis = st.selectbox("Select y-axis", options)

# st.divider()

# Add a summary sentence with the correlation coefficient
corr = df[x_axis].corr(df[y_axis])
st.subheader(f"The correlation coefficient is {corr:.2f}.")

# st.divider()

# Option for log or linear scale
scale_x = st.radio("Linear Scale for x-axis", (False, True), horizontal=True)
scale_y = st.radio("Linear Scale for y-axis", (False, True), horizontal=True)

# Create a scatterplot
fig = px.scatter(df, x=x_axis, y=y_axis, hover_name=df.index, log_x=scale_x, log_y=scale_y, trendline="ols",
                 title=f"{x_axis.split(' (')[0].upper()} vs. {y_axis.split(' (')[0].upper()} in 2020")

st.divider()

# Display the scatterplot
st.plotly_chart(fig)
