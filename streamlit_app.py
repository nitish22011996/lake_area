import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

# Load the CSV data
file_path = 'Area_f_2.csv'  # Replace with your file path
df = pd.read_csv(file_path)

# Set default Lake ID
default_lake_id = df['Lake_id'].iloc[0]  # Use the first Lake ID as default

# Streamlit App Title
st.title('Lake Monitoring - Water Area and Trends')

# Sidebar for user input
st.sidebar.subheader("Input Lake ID")
lake_id_input = st.sidebar.text_input("Enter a Lake ID:", value=str(default_lake_id))

# Sidebar for region filter
st.sidebar.subheader("Filter Lakes by Region (optional)")
min_lat = st.sidebar.number_input("Min Latitude", value=float(df['Lat'].min()), format="%.6f")
max_lat = st.sidebar.number_input("Max Latitude", value=float(df['Lat'].max()), format="%.6f")
min_lon = st.sidebar.number_input("Min Longitude", value=float(df['Lon'].min()), format="%.6f")
max_lon = st.sidebar.number_input("Max Longitude", value=float(df['Lon'].max()), format="%.6f")

# Filter dataframe based on region inputs
filtered_df = df[
    (df['Lat'] >= min_lat) & (df['Lat'] <= max_lat) &
    (df['Lon'] >= min_lon) & (df['Lon'] <= max_lon)
]

# Function to generate the plot
def plot_lake_data(lake_id):
    try:
        # Filter the dataframe for the given Lake ID
        lake_data = df[df['Lake_id'] == int(lake_id)]
        
        if lake_data.empty:
            st.error("No data available for the selected Lake ID.")
            return

        # Extract the time-series data
        time_columns = [col for col in df.columns if col.endswith(('_01', '_02', '_03', '_04', '_05', '_06', '_07', '_08', '_09', '_10', '_11', '_12'))]
        lake_data.loc[:, time_columns] = lake_data[time_columns].apply(pd.to_numeric, errors='coerce')  # Avoid SettingWithCopyWarning
        dates = [f"{col[:4]}-{col[5:7]}-01" for col in time_columns]
        dates = pd.to_datetime(dates, errors='coerce')
        water_area = lake_data[time_columns].values.flatten()

        # Plot
        st.subheader(f'Water Area for Lake ID {lake_id} Over Time')
        plt.figure(figsize=(10, 6))
        plt.plot(dates, water_area, marker='o', label='Water Area', color='tab:blue')
        plt.title(f"Water Area for Lake ID {lake_id} Over Time")
        plt.xlabel('Date')
        plt.ylabel('Water Area')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        st.pyplot(plt)
    except Exception as e:
        st.error(f"Error while plotting data: {e}")

# Generate the default plot
st.sidebar.markdown(f"Showing data for default Lake ID: **{default_lake_id}**")
plot_lake_data(default_lake_id)

# Map
st.subheader("Map of Lakes")
m = folium.Map(location=[df['Lat'].mean(), df['Lon'].mean()], zoom_start=6)

# Add MarkerCluster to the map for better performance
marker_cluster = MarkerCluster().add_to(m)

# Add markers for the filtered lakes
for _, row in filtered_df.iterrows():
    folium.Marker(
        location=[row['Lat'], row['Lon']],
        popup=f"Lake ID: {row['Lake_id']}",
        icon=folium.Icon(color='green')
    ).add_to(marker_cluster)

# Display the map
map_data = st_folium(m, width=700, height=500)

# Check for user clicks on map
if map_data and map_data.get('last_object_clicked') is not None:
    try:
        clicked_lake_id = map_data['last_object_clicked']['popup'].split(": ")[1]
        st.sidebar.markdown(f"**Lake ID {clicked_lake_id} selected from the map.**")
        plot_lake_data(clicked_lake_id)
    except Exception as e:
        st.error(f"Error processing map click: {e}")

# Update plot when user enters Lake ID
if lake_id_input:
    st.sidebar.markdown(f"**Lake ID {lake_id_input} entered manually.**")
    plot_lake_data(lake_id_input)

