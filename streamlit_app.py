# import required packages
import streamlit as st

import numpy as np
import pandas as pd
import geopandas as gpd
import altair as alt
import matplotlib.pyplot as plt
import matplotlib.colors as colors

# load required datasets
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world = world[['name', 'continent', 'geometry']]
data = pd.read_csv('tfr_dataset.csv') # world bank dataset
dataset = pd.merge(world, data, left_on = 'name', right_on = 'country', how = 'inner') # merged dataset

# These are the charts of the visualization

# chart 1.1, TFR in 1970
def chart1_1970(dataset):
    data = dataset[dataset['date'] == 1970]
    fig, ax = plt.subplots(figsize = (15, 5))
    cmap = colors.ListedColormap(['darkblue', 'lightblue', 'salmon', 'darkred', '#8B008B'])
    bounds = [0, 1.4, 1.8, 2.4, 5, 8]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    data.plot(column = 'tfr', cmap = cmap, linewidth = 0.8, ax = ax, edgecolor = '0.8', legend = True, norm = norm)
    ax.set_title('Total Fertility Rate in 1970')
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    st.pyplot(fig)
# chart 1.2, TFR in 2020
def chart1_2020(dataset):
    data = dataset[dataset['date'] == 2020]
    fig, ax = plt.subplots(figsize = (15, 5))
    cmap = colors.ListedColormap(['darkblue', 'lightblue', 'salmon', 'darkred', '#8B008B'])
    bounds = [0, 1.4, 1.8, 2.4, 5, 8]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    data.plot(column = 'tfr', cmap = cmap, linewidth = 0.8, ax = ax, edgecolor = '0.8', legend = True, norm = norm)
    ax.set_title('Total Fertility Rate in 2020')
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    st.pyplot(fig)
# chart 1.3, TFR difference between 1970 and 2020
def chart1_diff(dataset):
    data = dataset[dataset['date'] == 2020]
    fig, ax = plt.subplots(figsize = (15, 5))
    cmap = colors.ListedColormap(['darkblue', 'lightblue', 'salmon'])
    bounds = [-5, -3, -1, 0]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    data.plot(column = 'tfr_diff', cmap = cmap, linewidth = 0.8, ax = ax, edgecolor = '0.8', legend = True, norm = norm)
    ax.set_title('50 Years Total Fertility Rate Change')
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    st.pyplot(fig)
# chart 2, current TFR situation in 2020
def chart2_interact(dataset):
    data = dataset[dataset['date'] == 2020]
    data = data.drop('geometry', axis = 1)
    interval = alt.selection_interval()
    base_color_scale = alt.Scale(domain = [1, 2, 4, 6], range = ['darkblue', 'green', 'red', 'purple'])
    # base scatter chart, average GDP vs TFR
    base_chart = alt.Chart(data).mark_circle(size = 80).encode(
        x = alt.X('log_avg_gdp:Q', scale = alt.Scale(domain = (5, 12)), axis = alt.Axis(title='Log Average GDP')),
        y = alt.Y('tfr:Q', scale = alt.Scale(domain = (0.5, 7)), axis = alt.Axis(title = 'Total Fertility Rate')),
        color = alt.condition(interval, 'tfr:Q', alt.value('lightgray'), scale = base_color_scale, legend = alt.Legend(title = 'TFR')),
        tooltip = ['name:N', 'tfr:Q', 'population_density:Q']
    ).add_selection(interval).properties(
        width = 720,
        height = 360,
        title = 'Avg GDP vs. TFR'
    )
    # distribution of continents
    continent_chart = alt.Chart(data).mark_bar().encode(
        x = alt.X('count():Q', title = None),
        y = alt.Y('continent:N', title = None),
        tooltip = ['continent:N']
    ).transform_filter(interval).properties(
        width = 220,
        height = 220,
        title = 'Continents'
    )
    # visualization of key indices
    box_chart_1 = alt.Chart(data).mark_boxplot(extent = 'min-max').encode(
        x = alt.X('primary_education:Q', axis = alt.Axis(title = 'Primary Education Rate'), scale = alt.Scale(domain = [60, 140])),
        color = alt.value('orange')
    ).transform_filter(interval).properties(
        width = 400,
        height = 15,
    )
    box_chart_2 = alt.Chart(data).mark_boxplot(extent = 'min-max').encode(
        x = alt.X('female_male_labor:Q', axis = alt.Axis(title = 'Female Labor Participation'), scale = alt.Scale(domain = [20, 110])),
        color = alt.value('brown')
    ).transform_filter(interval).properties(
        width = 400,
        height = 15,
    )
    box_chart_3 = alt.Chart(data).mark_boxplot(extent = 'min-max').encode(
        x = alt.X('life_expectancy:Q', axis = alt.Axis(title = 'Life Expectancy'), scale = alt.Scale(domain = [50, 85])),
        color = alt.value('olive')
    ).transform_filter(interval).properties(
        width = 400,
        height = 15,
    )
    box_chart_4 = alt.Chart(data).mark_boxplot(extent = 'min-max').encode(
        x = alt.X('contraceptive_prevalence:Q', axis = alt.Axis(title = 'Contraceptive Prevalence'), scale = alt.Scale(domain = [10, 80])),
        color = alt.value('teal')
    ).transform_filter(interval).properties(
        width = 400,
        height = 15,
    )
    # combination of charts
    box_charts = box_chart_1 & box_chart_2 & box_chart_3 & box_chart_4
    sub_chart = box_charts | continent_chart
    return base_chart & sub_chart
# chart3, evolution of key indices of selected country/region
def chart3_display(data, country):
    selected = data[data['country'] == country]
    selected = selected[['date', 'tfr', 'avg_gdp', 'gini', 'population_density',
        'primary_education', 'secondary_education', 'contraceptive_prevalence',
        'life_expectancy', 'adolescent_fertility_rate', 'female_male_labor']]
    fig, ax1 = plt.subplots(figsize = (10, 6), dpi = 100)
    ax2 = ax1.twinx()
    ax3 = ax1.twinx()
    ax4 = ax1.twinx()
    ax5 = ax1.twinx()
    ax6 = ax1.twinx()
    ax7 = ax1.twinx()
    # Plot the lines on their respective axes
    ax1.plot(selected['date'], selected['tfr'], 'b-', label = 'TFR', linewidth = 2)
    ax2.plot(selected['date'], selected['avg_gdp'], 'r--', label = 'Avg GDP', linewidth = 2)
    ax3.plot(selected['date'], selected['gini'], 'g-.', label = 'Gini Index')
    ax4.plot(selected['date'], selected['primary_education'], 'c:', label = 'Primary Education Rate')
    ax5.plot(selected['date'], selected['life_expectancy'], 'm-.', label = 'Life Expectancy')
    ax6.plot(selected['date'], selected['adolescent_fertility_rate'], 'y:', label = 'Adolescent Fertility Rate')
    ax7.plot(selected['date'], selected['female_male_labor'], 'k--', label = 'Female Labor Participation')
    # Hide y-axis labels and ticks for all axes
    ax1.set_yticklabels([])
    ax2.set_yticklabels([])
    ax3.set_yticklabels([])
    ax4.set_yticklabels([])
    ax5.set_yticklabels([])
    ax6.set_yticklabels([])
    ax7.set_yticklabels([])
    # Set the plot titles
    ax1.set_title('Evolution of Indices')
    # Set the legend
    lines = [ax1.get_lines()[0], ax2.get_lines()[0], ax3.get_lines()[0], ax4.get_lines()[0], ax5.get_lines()[0], ax6.get_lines()[0], ax7.get_lines()[0]]
    labels = [line.get_label() for line in lines]
    plt.legend(lines, labels)
    # Adjust spacing between subplots
    fig.tight_layout()
    # Display the plot
    st.pyplot(fig)

# the following are the deployment of the application

st.title('Business Intelligence Final Project')
st.markdown('## Unraveling the Fertility-Economy Nexus')
st.write('**Author:** Yifan WANG')

st.write('---')

st.write("""
## Introduction

The **Total Fertility Rate** (TFR) is a significant demographic metric that represents *the number of children a woman is projected to give birth to during her lifetime*. It is a crucial parameter to understand population dynamics and trends, particularly in the context of economic and social indices.

In this project, we delve into **an analysis of TFR**, exploring its **evolution** and **relationship** with various other economic indices. The project draws on a comprehensive dataset sourced from the World Bank, examining the interplay between TFR and factors such as GDP, Gini index, population, population density, education levels, contraceptive prevalence, life expectancy, adolescent fertility rate, and female to male labor participation.

## Dataset Introduction

The dataset used in this project is derived from the World Bank through the `wbdata` package in Python. The selected indicators are:

1. 'SP.DYN.TFRT.IN': 'tfr' - Total Fertility Rate
2. 'NY.GDP.MKTP.CD': 'gdp' - Gross Domestic Product
3. 'SI.POV.GINI': 'gini' - Gini Index
4. 'SP.POP.TOTL': 'population' - Total Population
5. 'EN.POP.DNST': 'population_density' - Population Density
6. 'SE.PRM.ENRR': 'primary_education' - Primary Education Enrollment Rate
7. 'SE.SEC.ENRR': 'secondary_education' - Secondary Education Enrollment Rate
8. 'SP.DYN.CONU.ZS': 'contraceptive_prevalence' - Contraceptive Prevalence
9. 'SP.DYN.LE00.IN': 'life_expectancy' - Life Expectancy at Birth
10. 'SP.ADO.TFRT': 'adolescent_fertility_rate' - Adolescent Fertility Rate
11. 'SL.TLF.CACT.FM.ZS': 'female_male_labor' - Ratio of Female to Male Labor Force Participation Rate

## Tools Used

The project employed a suite of tools to manage dataset download, processing, and visualization:

- **Python**: Used for dataset download and processing.
- **Matplotlib**: Employed for basic data visualization.
- **Geopandas**: Utilized for visualizing the world map.
- **Altair**: Used for creating interactive charts.
- **Tableau**: Used for creating additional charts.
""")

st.write('---')

st.markdown('## Evolution of Total Fertility Rate (1970-2020)')

st.write("""
In this section, we present a **geographical visualization** of the evolution of Total Fertility Rate (TFR) over the course of 50 years, from 1970 to 2020. Three world maps are displayed, each representing the TFR scenario in 1970, 2020, and the change in TFR over the 50-year period. The TFR levels are color-coded, with **deep blue for low TFR**, **salmon for medium TFR**, **dark red for high TFR**, and **dark purple for extreme TFR**.
""")

# create a selectbox in the sidebar
option = st.sidebar.selectbox(
    'Which chart do you want to visualize?',
    ('Year 1970', 'Year 2020', 'TFR Difference'))

if option == 'Year 1970':
    chart1_1970(dataset)
elif option == 'Year 2020':
    chart1_2020(dataset)
else:
    chart1_diff(dataset)

st.write("""
The 1970 world map paints a vivid picture of **high fertility rates**. The canvas is predominantly red and purple, indicating high to extreme TFR. The regions of Canada, Russia, Eastern Europe, and Northern Europe stand out with medium (salmon) TFR levels, while the continents of Africa and Asia are awash in purple, indicative of extreme TFR.

Fast forward to 2020, the global TFR landscape has significantly transformed. The world map has cooled down, reflecting lower fertility rates. Most African countries have transitioned from purple to red, signifying a drop in TFR. Asia presents a remarkable shift with countries like China, South Korea, and Japan turning dark blue, reflecting low TFR. The difference map underscores this drastic decline in TFR, particularly in regions like Asia, the Middle East, North Africa, and Latin America.

This substantial decrease in TFR over the years may be attributed to a multitude of factors including improved access to education, especially for women, increased employment opportunities, advancements in contraceptive methods, and changing social norms. However, the effects of these changes can vary significantly across different regions, influenced by local cultural, economic, and social contexts. 
""")

st.write('---')

st.markdown('## Unpacking the Relationship between TFR and Economic Indicators')

st.write("""
In this section, we delve into the **interrelationships** between Total Fertility Rate (TFR) and a range of economic and social indicators. An interactive scatter plot forms the centerpiece, revealing a notable negative correlation between TFR and average GDP. Accompanying this are several subplots that explore the relationships between TFR and primary education, female to male labor participation, life expectancy, and contraceptive prevalence.
""")

st.altair_chart(chart2_interact(dataset), use_container_width = True)

st.write("""
The strong negative correlation between TFR and average GDP suggests that as nations become wealthier, they tend to have lower fertility rates. This could be attributed to multiple factors, such as increased access to education, improved healthcare, and changes in societal norms and expectations. 

The subplots further illuminate the dynamics at play. For instance, higher levels of primary education, particularly for girls, can often lead to lower fertility rates as education increases awareness and access to family planning methods.

However, it's crucial to note that the relationship between TFR and these indicators is complex and multifaceted. Fertility trends and their determinants can vary greatly across different regions and cultures, reflecting a blend of economic, social, and demographic factors. Despite the apparent global trend of declining TFR with improving economic conditions, the mechanisms driving these changes are not fully understood and warrant further research.
""")

st.write('---')

st.markdown('## Chart 3: Navigating through Country-Specific TFR Trends')

st.write("""
In this section, we offer an opportunity to delve into **country-specific trends**, showcasing the **evolution of key indicators** over the past 50 years. The ability to select a specific country/region allows for an exploration of the complex and unique factors influencing Total Fertility Rate (TFR) in different global contexts. 
""")

option = st.sidebar.selectbox(
    'Which country do you want to visualize?',
    tuple(data['country'].unique()))

chart3_display(data, option)

st.write("""
This country-specific approach uncovers the intricate nature of TFR determinants. For instance, while average GDP generally exhibits a negative correlation with TFR, certain countries like France present unique trends. Initially, France mirrors the typical pattern of falling TFR as GDP rises. However, at a certain point, this relationship reverses, and rising GDP accompanies an increasing TFR.

China presents another deviation, where the trend of average GDP doesn't necessarily align with the TFR trend. This could be attributed to various factors such as governmental policies, societal norms, and the cost of raising children, among others.

It becomes evident that the mechanisms affecting TFR are highly complex and can vary substantially across different countries and regions. For instance, in regions like South East Asia and Europe, the high costs associated with child-rearing have a significant negative impact on TFR. This underscores the importance of considering local socioeconomic and cultural contexts when examining fertility trends.

In conclusion, while there are clear global trends and common factors influencing TFR, the story of fertility rates is one of diversity and complexity. Each country has its unique narrative shaped by an interplay of various factors, reflecting the multifaceted nature of demographic changes.
""")

st.write('---')

st.markdown('## Conclusion')

st.write("""
Through this project, we embarked on an exploration of Total Fertility Rate (TFR) – a crucial demographic indicator. The journey took us through a global panorama of TFR evolution over the last 50 years, an analysis of TFR in relation to economic indicators, and finally, a deep dive into country-specific TFR trends. 

The visualizations underscored the profound transformation of global fertility rates, particularly noticeable in Asia, the Middle East, North Africa, and Latin America. The correlation analyses illuminated the complex interplay of factors influencing TFR, from GDP and education to female labor participation and contraceptive prevalence. However, the country-specific trends highlighted the unique narratives that each region has, demonstrating the multifaceted and intricate nature of TFR.

Understanding these trends and their implications is crucial for policymakers, demographers, and economists. For policymakers, insights from this project can inform strategies related to population growth, labor market planning, and social welfare. Demographers can use this analysis to understand past trends and project future demographic shifts. Economists may find the connections between economic indicators and fertility rate beneficial for studies related to economic development and growth.

In summary, while global trends provide a broad understanding of TFR dynamics, the story of fertility rates is nuanced, complex, and region-specific. This underlines the need for further research that takes into account the diverse socioeconomic and cultural contexts shaping fertility trends around the world.
""")