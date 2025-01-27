import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import folium
from folium.plugins import MarkerCluster

# Load the CSV data (uploaded file)
file_path = 'Area_f_2.csv'  # path to your newly uploaded file
df = pd.read_csv(file_path)

# App title
st.title('Lake Monitoring - Water Area and Seasonal Trends')

# Dropdown to select the lake ID
lake_id = st.selectbox('Select a Lake by ID:', df['Lake_id'].unique())

# Filter the dataframe by the selected lake ID
lake_data = df[df['Lake_id'] == lake_id]

# Display filtered lake information
st.write(f"Data for Lake ID: {lake_id}")
st.write(lake_data)

# Extract the columns for the monthly data (e.g., 1990_01, 1990_02, ...)
time_columns = [col for col in df.columns if col.endswith(('_01', '_02', '_03', '_04', '_05', '_06', '_07', '_08', '_09', '_10', '_11', '_12'))]

# Plot the Water Area over Time (or any other specific column) for the selected lake
st.subheader(f'Water Area for Lake ID {lake_id} Over Time')

# Manually convert 'YYYY_MM' format to 'YYYY-MM-01'
dates = [f"{col[:4]}-{col[5:7]}-01" for col in time_columns]

# Now use pandas to convert these to datetime objects
dates = pd.to_datetime([col for col in time_columns], format='%Y_%m')


# Assuming we're focusing on the column '1990_01', '1990_02', ..., as a water area proxy
water_area = lake_data[time_columns].values.flatten()

# Plot the Water Area vs. Date
plt.figure(figsize=(10, 6))
plt.plot(dates, water_area, marker='o', label='Water Area')
plt.title(f"Water Area for Lake ID {lake_id} Over Time")
plt.xlabel('Date')
plt.ylabel('Water Area')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
st.pyplot(plt)

# Optionally, you can also display seasonal trends or other data (e.g., temperature, precipitation)
st.subheader('Seasonal Trends')

# Display the seasonal trends for Jul-Oct, Mar-Jun, Nov-Feb
seasons = ['Jul-Oct_Pe', 'Jul-Oct_Tr', 'Jul-Oct_Ta', 'Mar-Jun_Pe', 'Mar-Jun_Tr', 'Mar-Jun_Ta', 'Nov-Feb_Pe', 'Nov-Feb_Tr', 'Nov-Feb_Ta']
for season in seasons:
    st.write(f"{season}: {lake_data[season].values[0]}")

# Create a map using Folium centered around the first lake's latitude and longitude (or average if multiple)
lat = lake_data['Lat'].values[0]
lon = lake_data['Lon'].values[0]

# Create a folium map centered around the selected lake's location
m = folium.Map(location=[lat, lon], zoom_start=6)

# Add a marker for the lake
folium.Marker(
    location=[lat, lon],
    popup=f"Lake ID: {lake_id}\nLatitude: {lat}\nLongitude: {lon}",
    icon=folium.Icon(color='blue')
).add_to(m)

# Optionally, you can add a marker cluster to handle multiple lakes if necessary
marker_cluster = MarkerCluster().add_to(m)

# Add all lake locations to the map (you can loop over the dataframe if you'd like to plot all lakes)
for _, row in df.iterrows():
    folium.Marker(
        location=[row['Lat'], row['Lon']],
        popup=f"Lake ID: {row['Lake_id']}\nLatitude: {row['Lat']}\nLongitude: {row['Lon']}",
        icon=folium.Icon(color='green')
    ).add_to(marker_cluster)

# Display the map in Streamlit
st.subheader('Map of Lake Locations')
st.write(m)


