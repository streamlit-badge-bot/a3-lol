import streamlit as st
import pandas as pd
import altair as alt

st.title("Let's analyze some Data about Majors and Jobs!")

@st.cache  # add caching so we load the data only once
def load_data():
    # Load the Major data from https://raw.githubusercontent.com/fivethirtyeight/data/master/college-majors/recent-grads.csv.
    recent_grad_url = "https://raw.githubusercontent.com/fivethirtyeight/data/master/college-majors/recent-grads.csv"
    return pd.read_csv(recent_grad_url)

df = load_data()

# st.write("Let's look at raw data in the Pandas Data Frame.")

# st.write(df)

st.write("Here is the visualization you can play with!")

# side bar #
useful_cols = [df.columns[i] \
               for i in range(len(df.columns)) if i not in [0,1,2,6]]

option_field = st.sidebar.selectbox(
    'Choose a field!',
     useful_cols)  

explanations = { "Total"        :"Total number of people with major",
                "Sample_size"   :"Sample size (unweighted) of full-time, year-round ONLY (used for earnings)",
                "Men"           :"Male graduates",
                "Women"         :"Female graduates",
                "ShareWomen"    :"Women as share of total",
                "Employed"      :"Number employed",
                "Full_time"     :"Employed 35 hours or more",
                "Part_time"     :"Employed less than 35 hours",
                "Full_time_year_round":"Employed at least 50 weeks and at least 35 hours",
                "Unemployed"    :"Number unemployed",
                "Unemployment_rate":"Unemployed / (Unemployed + Employed)",
                "Median"        :"Median earnings of full-time, year-round workers",
                "P25th"         :"25th percentile of earnings",
                "P75th"         :"75th percentile of earnings",
                "College_jobs"  :"Number with job requiring a college degree",
                "Non_college_jobs":"Number with job not requiring a college degree",
                "Low_wage_jobs" :"Number in low-wage service jobs"
                }

st.sidebar.write(explanations[option_field])

# side bar end #

# first visualization #

brush = alt.selection(type='interval', encodings=['y'])

chart = alt.Chart(df).mark_bar().encode(
    x=alt.X(option_field, scale=alt.Scale(zero=False),),
    y=alt.Y("Major", scale=alt.Scale(zero=False),
            sort = '-x', 
            axis=alt.Axis(labelOverlap=True)),
    color=alt.Y("Major_category"),
    opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.4)),
    tooltip=["Major", "Major_category", option_field]
).add_selection(
    brush
).properties(
    width=1000, height=750
)

line = alt.Chart(df).mark_rule(color='firebrick').encode(
    x='mean(' + option_field + '):Q',
    size=alt.SizeValue(3)
).transform_filter(
    brush
).properties(
    width=1000, height=750
)

st.write(alt.layer(chart, line))
# first visualization end #