# Project name

<!-- ![A screenshot of your application. Could be a GIF.](screenshot.png) -->

## Project Goals

<!-- TODO: **A clear description of the goals of your project.** Describe the question that you are enabling a user to answer. The question should be compelling and the solution should be focused on helping users achieve their goals.  -->

The main goal of our project is to enable users to find useful information about jobs and majors. Our main target users are those who start their college and need some job-related information to help them pick a major, or those who will graduate recently and try to find how competent is his/her major in the job market. Moreover, this project is also designed for researchers who want to investigate social issues in terms of jobs, gender and majors (e.g., Does median wages correlate to women share of a specific major?).


TODO: add specific compiling questions & solutions for our dataset


## Design

<!-- TODO: **A rationale for your design decisions.** How did you choose your particular visual encodings and interaction techniques? What alternatives did you consider and how did you arrive at your ultimate choices? -->

Firstly, our project provides a multi-select box to enable users to pick major categories they want to focus on investigating: for example, Engineering, Law, Mathematics, etc. The reason for this filter functionality is that instead of all majors, users probably tend to know information about some specific ones. In this way, users can filter out the undesired majors from the visualization to better focus on the selected ones.

We have two major visualizations to achieve our goals.

The first visualization demonstrates aggregated data with respect to majors and a user-controlled field (e.g., median wage). We also insert a red line which represents the average value of the selected field, enabling users to compare their target data with the mean of the selected field. Combining these visual encodings together could allow users to find answers about some complicated questions they raise: for example, “What’s the difference between the expected wage of my major and the average wages of the top 25% highest-wages majors?”. We thought about using scatter plots to visualize this data, but found that they are deficient to visually reflect different quantities, so we choose bar charts instead to help displaying this kind of information.

The second visualization is used for revealing statistical relationships between fields, which is served more as a tool than a conclusion drawn by the visualization makers. Three sub-visualizations build up the whole picture: the leftmost scatter plot reveals the distribution with respect to two fields, and the rest two bar charts shows the values of each field with respect to majors. Users can use the scatter plot to investigate the relationship between the selected two fields, and to examine whether there is any correlation between the two fields. At the first glance, the two bar charts are just redundant iterations of the data represented by the scatter plot. However, they are actually useful because:

-  it vividly shows the exact data with a user-defined region, in which points could be potentially closed to each other and hard to perceive the exact value
-  it helps distinguish the major categories of a selected region, as the area of a bar is much larger than a point.

<!-- Before using a scatter plot to show correlations and distributions, we discussed about only give users a overall graph showing the mathematical correlations of very pair of fields, but we finally quit from this approach because 1) doing this is nothing than giving a bunch of numbers and 2) some pairs of the field would not make sense at all. Hence, we chose to let the users themselves think about what they want to investigate. -->

TODO: add correlation & describe the purpose

## Development

<!-- TODO: **An overview of your development process.** Describe how the work was split among the team members. Include a commentary on the development process, including answers to the following questions: Roughly how much time did you spend developing your application (in people-hours)? What aspects took the most time? -->

1. Data selection: Both of the teammates investigated into several data sources and discuss potential visualizations for each datasets. A documentation was created to keep track of though processes along the way, including possible data sources to be used (for example, [World Bank data](https://data.worldbank.org/indicator), [Flight delay data](https://www.kaggle.com/usdot/flight-delays?select=flights.csv), and [College major data](https://github.com/fivethirtyeight/data/tree/master/college-majors)). We discussed potential visualizations for each sources, and then decided the final source dataset among the possible datasets. In total, the exploratory data analysis process took 15 hours.

2. Data understanding: After choosing the target dataset [College major data](https://github.com/fivethirtyeight/data/tree/master/college-majors), both teammates spent time on analyzing the nature of the data and figure out what are some interesting questions to be discovered by this kind of dataset. In total, it took 5 hours for us to determine what kind of visualization suit best for this dataset, and what are the valuable part should be presented to the users.

3. Implementation: Data fetching, filtering, and displaying are performed with Streamlit. Shaobo (shaobog) focused on creating visualizations on given data, and utilizing bar charts and scatter plots to display the dataset correspondingly. Yuxi (yuxiluo) focused on filtering the data, providing category selection to provide additional freedom for the users to manipulate the displayed data, and fine-tuning the final version of the website. Both of the teammates spent time to evaluate the current process and determine the next steps to improve current visualizations. In total, it took 20 hours for us to finalize the entire visualization.

The Implementation took the most time, because for each visualization we iteratively provided ideas to improve the visualizations. For each specific functionality, there were many bugs we spent time to work on so that the final implementation is bug-free and well-structured.
