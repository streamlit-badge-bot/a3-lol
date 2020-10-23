import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

######################### global tables ########################

explanations = { "Total"        :"Total: Total number of people with major",
                "Men"           :"Men: Male graduates",
                "Women"         :"Women: Female graduates",
                "Employed"      :"Employed: Number of employed",
                "Full_time"     :"Full_time: Employed 35 hours or more",
                "Part_time"     :"Part_time: Employed less than 35 hours",
                "Full_time_year_round":"Full_time_year_round: Employed at least 50 weeks and at least 35 hours",
                "Unemployed"    :"Unemployed: Number of unemployed",
                "Unemployment_rate":"Unemployment_rate: Unemployed / (Unemployed + Employed)",
                "Median"        :"Median: Median earnings of full-time, year-round workers",
                "P25th"         :"P25th: 25th percentile of earnings",
                "P75th"         :"P75th: 75th percentile of earnings",
                "College_jobs"  :"College_jobs: Number with job requiring a college degree",
                "Non_college_jobs":"Non_college_jobs: Number with job not requiring a college degree",
                "Low_wage_jobs" :"Low_wage_jobs: Number in low-wage service jobs"
                }
rev_explanations = { v : k for k, v in explanations.items() }

##################### end of global tables #####################

####################### helper functions #######################
@st.cache  # add caching so we load the data only once
def load_data():
    recent_grad_url = "https://raw.githubusercontent.com/fivethirtyeight/data/master/college-majors/recent-grads.csv"
    return pd.read_csv(recent_grad_url)

def draw_title():
    st.markdown(
    """
        # Lets's analyze some data about College Majors!

        Made by Shaobo Guan (shaobog) and Yuxi Luo (yuxiluo)
        - [Github repository](https://github.com/CMU-IDS-2020/a3-lol)
        - [Project WriteUp](https://github.com/CMU-IDS-2020/a3-lol/blob/master/writeup.md)

        ## Project Overview

        Nowadays students have a wide range of majors that they can pursue as a college student. However, will every college majors ensure similar economic standing after graduation? We want to investigate into the relationship between college majors and their corresponding economic status. The dataset [College Majors](https://github.com/fivethirtyeight/data/blob/master/college-majors/recent-grads.csv) we chose contains information about a total of 173 college majors, including various statistics to quantitatively describe a major from an economic perspective. For example, it contains median earnings for each majors. The statistics allow us to understand college majors and the corresponding economic income after graduation.

        In particular, as students of the School of Computer Science at Carnegie Mellon University, we want to figure out whether our major is the most profitable major among all of the 173 college majors :)

        Several other interesting questions can be investigated while playing around with the tool we built:

        - Are STEM majors more profitable than other majors?
        - Are there less women in STEM majors?
        - Do any of two statistics have some correlations between each other?
    """
    )

def draw_selection(selection):
    st.sidebar.markdown(
    """
    ### Major Categories selection
    """
    )
    selected = st.sidebar.multiselect("Choose some major categories to explore!", selection, default=selection)
    return selected

def draw_major_statistics(df, selected, useful_cols):
    # first visualization #
    st.markdown(
    """
    ## Let's explore various statistics of all majors!

    #### Instructions for use:
    - From the sidebar on the left, you can narrow down the major categories as you wish, by selecting / deselecting them to interact with filtered data
    - You can choose a field to view the statistics of all majors
    - The red line on the graph indicates the average value of all majors
    - You can also select a range of specific majors to measure the average value of of the statistics
    """
    )

    filtered_df = df.loc[df["Major_category"].isin(selected)]

    # select box #
    option_field = rev_explanations[st.selectbox('Choose a field!', useful_cols)]

    avg_brush = alt.selection(type='interval', encodings=['y'])

    chart = alt.Chart(filtered_df).mark_bar().encode(
        x=alt.X(option_field, scale=alt.Scale(zero=False),),
        y=alt.Y("Major", scale=alt.Scale(zero=False),
                sort = '-x',
                axis=alt.Axis(labelOverlap=True)),
        color=alt.Y("Major_category"),
        opacity=alt.condition(avg_brush, alt.OpacityValue(1), alt.OpacityValue(0.4)),
        tooltip=["Major", "Major_category", option_field]
    ).add_selection(
        avg_brush
    ).properties(
        width=1000, height=750
    )

    avg_line = alt.Chart(filtered_df).mark_rule(color='firebrick').encode(
        x='mean(' + option_field + '):Q',
        size=alt.SizeValue(3)
    ).transform_filter(
        avg_brush
    ).properties(
        width=1000, height=750
    )

    visual_1 = alt.layer(chart, avg_line)

    st.write(visual_1)
    # first visualization end #

def draw_correlations(df, selected, useful_cols):
    st.write(
    """
    ## Let's discover correlations between any two statistics of your choice!
    """
    )
    st.write(
    """
    ### Correlation matrix for all statistics

    To explore potential correlations among all statistics, a correlation matrix is calculated to check whether any two of the statistics correlate with each other. The matrix is visualized as below, with their correlation values colored from light to dark. As the color goes darker, the two statistics are more correlated with each other.

    This correlation graph serves as a reference for users to explore potential correlations between any two statistics. Some findings we discovered while analyzing the graph are listed below. It would be also interesting to look at the statistics under specific major categories. We also encourage users to explore and discover more insighs about the statistics!
    - Low Wage Jobs is highly correlated with Non-College Jobs
    - College Jobs is more correlated with Women than Men
    - (more to be discovered)
    """
    )
    draw_corr_heatmap(df, selected, useful_cols)

    st.write(
    """
    ### Scatter plot for two statistics of your choice

    #### Instructions for use:
    - From the sidebar on the left, you can narrow down the major categories as you wish, by selecting / deselecting them to interact with filtered data
    - You can choose any of the two fields to explore the potential correlation between them
    - There are two subvisualizations to help investigating the exact value of the selected fields
    - You can also select a range of specific majors to closely look at the corresponding values from the two subvisualizations
    """
    )
    draw_corr_scatter(df, selected, useful_cols)

def draw_corr_heatmap(df, selected, useful_cols):
    filtered_df = df.loc[df["Major_category"].isin(selected)]
    discarded = ['Rank', 'Major_code', 'Major', 'Major_category', 'Sample_size', 'ShareWomen']
    for i in discarded:
        filtered_df = filtered_df.drop(i, axis=1)
    # calculate correlation
    corr = filtered_df.corr()
    x, y = np.meshgrid(corr.index, corr.columns)
    corr_df = pd.DataFrame({
        "FieldsX": x.ravel(),
        "FieldsY": y.ravel(),
        "Correlation": corr.values.ravel(),
    })
    # plot heatmap
    chart = alt.Chart(corr_df).mark_rect().encode(
        x="FieldsX:O",
        y="FieldsY:O",
        color=alt.Color("Correlation:Q", scale=alt.Scale(scheme='yellowgreenblue')),
        tooltip=["FieldsX", "FieldsY", "Correlation"]
    ).properties(
        width=650, height=550
    )
    st.write(chart)

def draw_corr_scatter(df, selected, useful_cols):
    # second visualization #
    filtered_df = df.loc[df["Major_category"].isin(selected)]

    # select box #
    option_field_x = rev_explanations[st.selectbox('Choose a field for the x-axis!', useful_cols)]
    option_field_y = rev_explanations[st.selectbox('Choose a field for the y-axis!', useful_cols)]

    brush = alt.selection(type = 'interval')

    corr = alt.Chart(filtered_df).mark_point().encode(
        x=alt.X(option_field_x+":Q",
                scale=alt.Scale(zero=False),
                axis=alt.Axis(labelOverlap=True),
                ),
        y=alt.Y(option_field_y+":Q",
                scale=alt.Scale(zero=False),
                axis=alt.Axis(labelOverlap=True),
                ),
        opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.1)),
        color=alt.Y("Major_category"),
        tooltip=["Major", option_field_y, option_field_x]
    ).add_selection(
        brush
    ).properties(
        width=850, height=400
    )

    support_chart = alt.Chart(filtered_df).mark_bar().encode(
        x=alt.X("Major", scale=alt.Scale(zero=False),
                sort = '-y',
                axis=alt.Axis(labelOverlap=True)),
        color=alt.condition(brush,
                            alt.Color('Major_category:N', legend=None),
                            alt.value('lightgray')),
        tooltip=["Major", "Major_category"],
    ).properties(
        width=400, height=300
    )

    visual_2 = corr & \
        (support_chart.encode(y=alt.Y(option_field_x, scale=alt.Scale(zero=False))) | \
        support_chart.encode(y=alt.Y(option_field_y, scale=alt.Scale(zero=False))))


    st.write(visual_2)
    # second visualization end #

####################### end of helper functions #######################
df = load_data()
categories = df["Major_category"].unique()
useful_cols = [explanations[df.columns[i]] for i in range(len(df.columns)) \
                if df.columns[i] not in ['Rank', 'Major_code', 'Major', \
                'Major_category', 'Sample_size', 'ShareWomen']]

draw_title()
selected = draw_selection(list(categories))
draw_major_statistics(df, selected, useful_cols)
draw_correlations(df, selected, useful_cols)
