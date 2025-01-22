import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import seaborn as sns
from io import BytesIO
import plotly.express as px 
import folium
from folium.plugins import HeatMap, MarkerCluster
from folium import Choropleth, Circle
import streamlit as st

tab1,tab2,tab3 = st.tabs(["plotly","geopandas","folium"])

gdf = gpd.read_file("NGA_health.shp")

boundaries = gpd.read_file('boundary.shp')

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
            size=6,  # Font size for legend text
            color="black"  # Font color
        ),
        itemwidth=30,
        bgcolor=None,  # Background color
        bordercolor=None,  # Border color
        borderwidth=0.5,  # Border width
        tracegroupgap=0.1
    )
)


fig.update_traces(
    textposition = 'outside',
    texttemplate = '%{y}'
)

tab1.plotly_chart(fig, use_container_width= False)

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
            size=6,  # Font size for legend text
            color="black"  # Font color
        ),
        itemwidth = 30,
        bgcolor=None,  # Background color
        bordercolor=None,  # Border color
        borderwidth=0,  # Border width
        tracegroupgap = 0
    )
)


fig.update_traces(
    texttemplate = '%{y}'
)

tab1.plotly_chart(fig, use_container_width=False)

df1 = gdf.groupby(['ownership','Geo_zones'])['ownership_'].count().reset_index()

df1['count'] = df1['ownership_']
df1 = df1.drop('ownership_',axis = 1)

fig = px.bar(data_frame=df1,
              x='Geo_zones',
              y='count', 
              color= 'ownership',
             barmode= 'stack')

fig.update_layout(
    width = None,
    height = 500,
    xaxis_title = 'Geopolitical Zones',
    title = "Stacked bar Plot to check the Geo political zones against ownership of health centers"
)

fig.update_traces(
    texttemplate = '%{y}'
)

tab1.plotly_chart(fig, use_container_width=False)

colors = {"Public" : 'green',"Private" : 'blue', "Unknown" : 'red' }


fig,ax = plt.subplots(figsize=(14,10))
gdf.plot(column= 'ownership', ax=ax, color= gdf['ownership'].map(colors), edgecolor='grey')
boundaries.plot(ax=ax, color = 'None')
legend_handles = [Patch(color=color, label= ownership) for ownership, color in colors.items()]
ax.legend(
    handles=legend_handles,
    title="ownership",
    loc="lower right",
    fontsize=10,
    title_fontsize=12,
)
ax.set_title("Nigeria Health Facilities Ownership Map")

buffer = BytesIO()

plt.savefig(buffer,format='png',bbox_inches = 'tight')

buffer.seek(0)

tab2.image(buffer,use_container_width=True)

color_zones = {
    "North West" : 'green',
    "North Central" : 'yellow',
    "South West" : 'brown',
    "South East" : 'blue',
    "North East": 'grey',
    "South South" : 'black'}


fig,ax = plt.subplots(figsize=(14,10))
gdf.plot(column= 'Geo_zones', ax=ax, color= gdf['Geo_zones'].map(color_zones), edgecolor='grey')
boundaries.plot(ax=ax, color = 'None')
legend_handles = [Patch(color=color, label= zones) for zones, color in color_zones.items()]
ax.legend(
    handles=legend_handles,
    title="Geo_zones",
    loc="lower right",
    fontsize=10,
    title_fontsize=12,
)
ax.set_title("Nigeria Health Facilities Zones Map")

buffer = BytesIO()

plt.savefig(buffer,format='png',bbox_inches = 'tight')

buffer.seek(0)

tab2.image(buffer,use_container_width=True)

color_purpose = {
    "Federal Government" : 'green',
    "Local Government" : 'yellow',
    "Not For Profit" : 'orange',
    "State Government" : 'blue',
    "For Profit": 'grey',
    "Military & Paramilitary formations" : 'black',
    "Unknown" : 'red'}


fig,ax = plt.subplots(figsize=(14,10))
gdf.plot(column= 'ownership_', ax=ax, color= gdf['ownership_'].map(color_purpose), edgecolor='grey')
boundaries.plot(ax=ax, color = 'None')
legend_handles = [Patch(color=color, label= purpose) for purpose, color in color_purpose.items()]
ax.legend(
    handles=legend_handles,
    title="Purpose",
    loc="lower right",
    fontsize=10,
    title_fontsize=12,
)
ax.set_title("Nigeria Health Facilities Purpose Map")

buffer = BytesIO()

plt.savefig(buffer,format='png',bbox_inches = 'tight')

buffer.seek(0)

tab2.image(buffer,use_container_width=True)

