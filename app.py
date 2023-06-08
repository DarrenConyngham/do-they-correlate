import streamlit as st
import plotly.express as px
import pandas as pd
import statsmodels

st.title("Do They Correlate?")
st.subheader("Do Two World Development Indicators have a relationship?")

# Create a DataFrame
df = pd.read_parquet('WDIData2020reduced.parquet')

st.write("SELECT TWO VARIABLES TO COMPARE")

# Create a dropdown menu for the x-axis
options = df.columns
x_axis = st.selectbox("Select x-axis:", options)

# Create a dropdown menu for the y-axis
y_axis = st.selectbox("Select y-axis:", options)

st.divider()

# Add a summary sentence with the correlation coefficient
r = df[x_axis].corr(df[y_axis]).round(2)


def categorise_correlation_coefficient(r):
    """Categorise the correlation coefficient into weak, moderate or strong."""
    if abs(r) > 0.7:
        strength = 'strong'
    elif abs(r) > 0.4:
        strength = 'moderate'
    else:
        strength = 'weak'

    direction = 'positive' if r > 0 else 'negative'

    return f"{strength} {direction}"

st.write("RESULT")

st.markdown(f"""The correlation coefficient is **{r}**, which indicates a {categorise_correlation_coefficient(r)} relationship between the two variables.
    The R-squared value is **{round(r**2, 2)}**, meaning approximately **{round(r**2*100)}%** of the variation in one variable can be explained by the other.""")

st.divider()

st.write("SCATTER PLOT")

# Option for log or linear scale
scale_x = st.radio("Log Scale for x-axis:", (False, True), horizontal=True)
scale_y = st.radio("Log Scale for y-axis:", (False, True), horizontal=True)

# Create a scatterplot
fig = px.scatter(df.reset_index(), x=x_axis, y=y_axis, hover_name='Country Name',
                 log_x=scale_x, log_y=scale_y, trendline="ols", color='Region', trendline_scope='overall', opacity=0.8,
                 title=f"{x_axis.split(' (')[0].upper()} vs. {y_axis.split(' (')[0].upper()}")

# st.divider()

# Display the scatterplot
st.plotly_chart(fig)
st.caption(body="Source: World Bank, 2020")
