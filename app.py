import streamlit as st
import plotly.express as px
import pandas as pd
import statsmodels

st.title("Do They Correlate? :thinking_face:")
# st.markdown("### Do 2 World Development Indicators have a relationship?")

st.markdown("#### INTRODUCTION :wave:")

st.markdown("""Do richer countries have higher birth rates? Do older countries smoke more? This app uses World Bank [country-level data](https://data.worldbank.org/) from 2020 to answer these questions and many others! 
            Hopefully giving you a better understanding of the world :globe_with_meridians:.""")

# Create a DataFrame
df = pd.read_parquet('WDIData2020reduced.parquet')

st.divider()

st.markdown("#### SELECT TWO VARIABLES TO COMPARE :mag_right:")

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
    elif abs(r) > 0.3:
        strength = 'moderate'
    else:
        strength = 'weak'

    direction = 'positive' if r > 0 else 'negative'

    return f"{strength} {direction}"


st.markdown("#### RESULTS IN PLAIN ENGLISH :white_check_mark:")

st.markdown(f"""The correlation coefficient is **{r}**, which indicates a {categorise_correlation_coefficient(r)} relationship between the two variables.
    The R-squared value is **{round(r**2, 2)}**, meaning approximately **{round(r**2*100)}%** of the variation in one variable can be explained by the other.""")

st.divider()

st.markdown("#### CHART :chart_with_upwards_trend:")

# Option for log or linear scale
scale_x = st.radio("Log Scale for x-axis:", (False, True), horizontal=True)
scale_y = st.radio("Log Scale for y-axis:", (False, True), horizontal=True)

# Create a scatterplot
fig = px.scatter(df.reset_index(), x=x_axis, y=y_axis, hover_name='Country Name',
                 log_x=scale_x, log_y=scale_y, trendline="ols", color='Region', trendline_scope='overall', opacity=0.8)
fig.update_layout(title={
    'text': f"{x_axis.split(' (')[0].upper()} vs. {y_axis.split(' (')[0].upper()}",
    'y': 0.9,  # new
    'x': 0.5,
    'xanchor': 'center',
    'yanchor': 'top'  # new
})

# title_text=f"{x_axis.split(' (')[0].upper()} vs. {y_axis.split(' (')[0].upper()}", title_x=0.5, title_y=0.9,
#                title_x_anchor='center', title_y_anchor='top')


# Display the scatterplot
st.plotly_chart(fig)
st.caption(body="Source: World Bank, 2020")

st.divider()

st.markdown("#### OLS REGRESSION TABLE (THE VERY NERDY STUFF :nerd_face:)")

st.markdown(
    f"""The regression table below shows the results of a linear regression model with *{x_axis.split(' (')[0]}* as the independent variable and *{y_axis.split(' (')[0]}* as the dependent variable.""")

# Create a regression table
df = df.dropna(subset=[x_axis, y_axis]).reset_index()
X = df[x_axis]
y = df[y_axis]
X = statsmodels.api.add_constant(X)

model = statsmodels.api.OLS(y, X)
results = model.fit()
st.text(results.summary())


st.divider()

st.markdown("#### ABOUT THIS APP :information_source:")

st.markdown("""This app was created by [Darren Conyngham](https://darrenconyngham.github.io/cv/). It was built using [Streamlit](https://streamlit.io/) and many Python packages including Statsmodels, Pandas and Plotly. 
The data was sourced from the [World Bank](https://data.worldbank.org/) and the code is available on [GitHub](https://github.com/DarrenConyngham/do-they-correlate).""")