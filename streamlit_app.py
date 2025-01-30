import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

# Load the CSV data
file_path = 'Area_final.csv'  # Replace with your file path
df = pd.read_csv(file_path)

# Streamlit App Title
st.title('Lake Monitoring - Water Area and Trends')

# Sidebar for state selection
st.sidebar.subheader("Select State and District")
states = df['STATE'].unique()
selected_state = st.sidebar.selectbox("Select a State:", states)

# Filter districts based on selected state
districts = df[df['STATE'] == selected_state]['District'].unique()
selected_district = st.sidebar.selectbox("Select a District:", districts)

# Filter lakes based on selected district
filtered_df = df[(df['STATE'] == selected_state) & (df['District'] == selected_district)]

# Function to generate the plot
def plot_lake_data(lake_id):
    try:
        lake_data = df[df['Lake_id'] == int(lake_id)]
        if lake_data.empty:
            st.error("No data available for the selected Lake ID.")
            return

        time_columns = [col for col in df.columns if col.endswith(('_01', '_02', '_03', '_04', '_05', '_06', '_07', '_08', '_09', '_10', '_11', '_12'))]
        lake_data[time_columns] = lake_data[time_columns].apply(pd.to_numeric, errors='coerce')
        dates = [f"{col[:4]}-{col[5:7]}-01" for col in time_columns]
        dates = pd.to_datetime(dates, errors='coerce')
        water_area = lake_data[time_columns].values.flatten()

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

# Map
st.subheader("Map of Lakes in Selected District")
m = folium.Map(location=[filtered_df['Lat'].mean(), filtered_df['Lon'].mean()], zoom_start=8)
marker_cluster = MarkerCluster().add_to(m)

for _, row in filtered_df.iterrows():
    folium.Marker(
        location=[row['Lat'], row['Lon']],
        popup=f"Lake ID: {row['Lake_id']}",
        icon=folium.Icon(color='green')
    ).add_to(marker_cluster)

map_data = st_folium(m, width=700, height=500)

# Check for user clicks on map
if map_data and map_data.get('last_object_clicked') is not None:
    try:
        clicked_lake_id = map_data['last_object_clicked']['popup'].split(": ")[1]
        st.sidebar.markdown(f"**Lake ID {clicked_lake_id} selected from the map.**")
        plot_lake_data(clicked_lake_id)
    except Exception as e:
        st.error(f"Error processing map click: {e}")


