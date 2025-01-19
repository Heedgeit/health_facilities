import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px 
import folium
from folium.plugins import HeatMap, MarkerCluster
from folium import Choropleth, Circle
import streamlit as st

tab1,tab2,tab3 = st.tabs(["pie","bar","grouped bar"])

gdf = gpd.read_file("NGA_health.shp")

ss = ['Bayelsa','Rivers','Delta','Cross River','Akwa Ibom','Edo']
se = ['Abia','Anambra','Ebonyi','Enugu','Imo']
sw = ['Lagos','Oyo','Ogun','Ondo','Osun','Ekiti']
nc = ['Kwara','Kogi','Benue','Plateau','Niger','Nasarawa','Fct']
nw = ['Kano','Kaduna','Katsina','Kebbi','Sokoto','Jigawa','Zamfara']
ne = ['Adamawa','Bauchi','Borno','Gombe','Taraba','Yobe']

gz = []

for i in gdf.state :
    if i in ss :
        gz.append("South South")
    elif i in se :
        gz.append("South East")
    elif i in sw :
        gz.append("South West")
    elif i in nc :
        gz.append("North Central")
    elif i in nw :
        gz.append("North West")
    else :
        gz.append("North East")


gdf['Geo_zones'] = gz

zones_values = [i for i in gdf.Geo_zones.value_counts()]
zones = list(gdf.Geo_zones.value_counts().index)


pie_data = {'Zone Names': zones, 'Values': zones_values}


fig = px.pie(
    data_frame= pie_data,
    names= 'Zone Names',
    values= 'Values', 
    title= "Count of Hospitals along Geo Political Zones in Nigeria",
    hole= .7
)

fig.update_layout(
    width=600,   # Width of the chart
    height=600,  # Height of the chart
    title_font_size=14,  # Font size of the title
    title_x=0.2  # Center the title
)
fig.update_traces(
    textinfo="value+percent",  # Display labels and values
    textfont_size=14,       # Font size for the text
    textposition="inside"   # Position values inside the slices
)
tab1.plotly_chart(fig, use_container_width= True)


ownership_values = [i for i in gdf.ownership_.value_counts()]
ownership = list(gdf.ownership_.value_counts().index)

own = {'Ownership': ownership, 'Values': ownership_values}

fig = px.bar(
    data_frame= own,
    x= 'Ownership',
    y= 'Values',
    color = 'Ownership',
    title = 'Health Centers Ownership distributions'
)
fig.update_layout(
    width=None,   # Width of the chart
    height=600,  # Height of the chart
    title_font_size=14,  # Font size of the title
    title_x=0.0,  # Center the title,
    legend=dict(
        x=1.0,  # Position on the horizontal axis (0: left, 1: right)
        y=0.7,  # Position on the vertical axis (0: bottom, 1: top)
        xanchor="center",  # Horizontal anchor ('auto', 'left', 'center', 'right')
        yanchor="middle",  # Vertical anchor ('auto', 'top', 'middle', 'bottom')
        font=dict(
            size=9,  # Font size for legend text
            color="blue"  # Font color
        ),
        bgcolor="lightgrey",  # Background color
        bordercolor="black",  # Border color
        borderwidth=1,  # Border width
    )
)


fig.update_traces(
    textposition = 'outside',
    texttemplate = '%{y}'
)

tab2.plotly_chart(fig, use_container_width= False)

df = gdf.groupby(['Geo_zones','ownership_',])['facility_1'].count().reset_index()


df['count'] = df['facility_1']
df = df.drop('facility_1',axis = 1)


fig = px.bar(data_frame=df,
              x='ownership_',
              y='count', 
              color= 'Geo_zones',
             barmode= 'group')

fig.update_layout(
    width = None,
    height = 500,
    xaxis_title = 'Purpose',
    title = "Grouped bar Plot to check the Geo political zones against purpose of health centers",
    title_font_size=14,  # Font size of the title
    title_x=0.0,  # Center the title,
    legend=dict(
        x=0.6,  # Position on the horizontal axis (0: left, 1: right)
        y=0.7,  # Position on the vertical axis (0: bottom, 1: top)
        xanchor="center",  # Horizontal anchor ('auto', 'left', 'center', 'right')
        yanchor="middle",  # Vertical anchor ('auto', 'top', 'middle', 'bottom')
        font=dict(
            size=9,  # Font size for legend text
            color="blue"  # Font color
        ),
        bgcolor="lightgrey",  # Background color
        bordercolor="black",  # Border color
        borderwidth=1,  # Border width
    )
)


fig.update_traces(
    texttemplate = '%{y}'
)

tab3.plotly_chart(fig, use_container_width=False)