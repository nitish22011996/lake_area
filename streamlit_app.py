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

# Ensure column names are clean (remove spaces, convert to uppercase if needed)
df.columns = df.columns.str.strip()

# Sort states and districts for dropdown selection
df['STATE'] = df['STATE'].astype(str)
df['District'] = df['District'].astype(str)
sorted_states = sorted(df['STATE'].unique())  # Sort state list
default_state = sorted_states[0]  # Set first state as default

# Sidebar: Select State
st.sidebar.subheader("Select State")
selected_state = st.sidebar.selectbox("Choose a State:", sorted_states, index=0)

# Filter districts based on selected state
filtered_districts = df[df['STATE'] == selected_state]['District'].unique()
sorted_districts = sorted(filtered_districts)
default_district = sorted_districts[0]  # Set first district as default

# Sidebar: Select District
st.sidebar.subheader("Select District")
selected_district = st.sidebar.selectbox("Choose a District:", sorted_districts, index=0)

# Filter lakes based on selected district
filtered_lakes = df[(df['STATE'] == selected_state) & (df['District'] == selected_district)]

# Ensure at least one lake is selected by default
if filtered_lakes.empty:
    st.error("No lakes available for the selected State and District.")
    st.stop()

lake_ids = sorted(filtered_lakes['Lake_id'].unique())
default_lake_id = lake_ids[0]

# Sidebar: Select Lake ID
st.sidebar.subheader("Select Lake ID")
selected_lake_id = st.sidebar.selectbox("Choose a Lake ID:", lake_ids, index=0)

# Function to plot lake water area time series
def plot_lake_data(lake_id):
    try:
        lake_data = df[df['Lake_id'] == lake_id]

        if lake_data.empty:
            st.error("No data available for the selected Lake ID.")
            return

        # Extract the time-series data
        time_columns = [col for col in df.columns if col.endswith(tuple([f'_{i:02d}' for i in range(1, 13)]))]
        lake_data[time_columns] = lake_data[time_columns].apply(pd.to_numeric, errors='coerce')

        # Generate date labels
        dates = [f"{col[:4]}-{col[5:7]}-01" for col in time_columns]
        dates = pd.to_datetime(dates, errors='coerce')
        water_area = lake_data[time_columns].values.flatten()

        # Interpolate missing values
        water_area = pd.Series(water_area).interpolate(method='linear')

        # Plot
        st.subheader(f'Water Area for Lake ID {lake_id} Over Time')
        plt.figure(figsize=(10, 6))
        plt.plot(dates, water_area, marker='o', linestyle='-', color='tab:blue', label='Water Area')
        plt.xlabel('Date')
        plt.ylabel('Water Area')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        st.pyplot(plt)
    except Exception as e:
        st.error(f"Error while plotting data: {e}")

# Display water area time series for selected lake
plot_lake_data(selected_lake_id)

# Display map with filtered lakes for the selected district
st.subheader(f"Map of Lakes in {selected_district}, {selected_state}")
m = folium.Map(location=[filtered_lakes['Lat'].mean(), filtered_lakes['Lon'].mean()], zoom_start=7)

# Add markers for filtered lakes
marker_cluster = MarkerCluster().add_to(m)

for _, row in filtered_lakes.iterrows():
    folium.Marker(
        location=[row['Lat'], row['Lon']],
        popup=f"Lake ID: {row['Lake_id']}",
        icon=folium.Icon(color='green')
    ).add_to(marker_cluster)

# Display map
st_folium(m, width=700, height=500)
