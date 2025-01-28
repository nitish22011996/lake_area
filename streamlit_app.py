import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster
from datetime import datetime

# Load the CSV data
file_path = 'Area_f_2.csv'  # Replace with your file path
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

# Extract columns for monthly data (e.g., 1990_01, 1990_02, ...)
time_columns = [col for col in df.columns if col.endswith(('_01', '_02', '_03', '_04', '_05', '_06', '_07', '_08', '_09', '_10', '_11', '_12'))]

# Handle missing values in the monthly data
lake_data[time_columns] = lake_data[time_columns].apply(pd.to_numeric, errors='coerce')

# Plot the Water Area over Time
st.subheader(f'Water Area for Lake ID {lake_id} Over Time')

# Convert time column names to datetime objects (e.g., '1990_01' to '1990-01-01')
dates = [datetime.strptime(f"{col[:4]}-{col[5:7]}-01", "%Y-%m-%d") for col in time_columns]

# Flatten the water area data
water_area = lake_data[time_columns].values.flatten()

# Handle missing values in water area
water_area = pd.Series(water_area).interpolate(method='linear').fillna(0).values

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(dates, water_area, marker='o', label='Water Area', color='tab:blue')
plt.title(f"Water Area for Lake ID {lake_id} Over Time")
plt.xlabel('Date')
plt.ylabel('Water Area')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
st.pyplot(plt)

# Seasonal trends
st.subheader('Seasonal Trends')
seasons = ['Jul-Oct_Pe', 'Jul-Oct_Tr', 'Jul-Oct_Ta', 'Mar-Jun_Pe', 'Mar-Jun_Tr', 'Mar-Jun_Ta', 'Nov-Feb_Pe', 'Nov-Feb_Tr', 'Nov-Feb_Ta']

for season in seasons:
    if season in lake_data.columns:
        value = lake_data[season].values[0]
        st.write(f"{season}: {value if not pd.isna(value) else 'No data available'}")

# Map of lake locations
st.subheader('Map of Lake Locations')

# Center map on the selected lake
lat = lake_data['Lat'].values[0]
lon = lake_data['Lon'].values[0]
m = folium.Map(location=[lat, lon], zoom_start=6)

# Add a marker for the selected lake
folium.Marker(
    location=[lat, lon],
    popup=f"Lake ID: {lake_id}\nLatitude: {lat}\nLongitude: {lon}",
    icon=folium.Icon(color='blue')
).add_to(m)

# Add a marker cluster for all lakes
marker_cluster = MarkerCluster().add_to(m)

for _, row in df.iterrows():
    folium.Marker(
        location=[row['Lat'], row['Lon']],
        popup=f"Lake ID: {row['Lake_id']}\nLatitude: {row['Lat']}\nLongitude: {row['Lon']}",
        icon=folium.Icon(color='green')
    ).add_to(marker_cluster)

# Display the map
folium_static = st.components.v1.html(m._repr_html_(), height=600)
