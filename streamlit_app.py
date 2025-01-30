import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium

# Load the CSV data
file_path = 'Area_f_2.csv'  # Replace with your file path
df = pd.read_csv(file_path)

# Clean column names (strip spaces)
df.columns = df.columns.str.strip()

# Check if required columns exist
required_columns = {'STATE', 'District', 'Lake_id', 'Lat', 'Lon'}
if not required_columns.issubset(df.columns):
    st.error(f"Missing required columns: {required_columns - set(df.columns)}")
    st.stop()

# Streamlit App Title
st.title('Lake Monitoring - Water Area and Trends')

# Sidebar for user selection
st.sidebar.subheader("Select Filters")

# Step 1: Choose State (sorted list)
states = sorted(df['STATE'].dropna().unique())
default_state = states[0] if states else None
selected_state = st.sidebar.selectbox("Select a State:", states, index=states.index(default_state) if default_state else 0)

# Step 2: Choose District (filtered by selected state & sorted)
districts = sorted(df[df['STATE'] == selected_state]['District'].dropna().unique())
default_district = districts[0] if districts else None
selected_district = st.sidebar.selectbox("Select a District:", districts, index=districts.index(default_district) if default_district else 0)

# Filter lakes in the selected district
lakes_in_district = df[(df['STATE'] == selected_state) & (df['District'] == selected_district)]

# Step 3: Display all lake locations on the map
st.subheader(f"Lakes in {selected_district}")
if not lakes_in_district.empty:
    m = folium.Map(location=[lakes_in_district['Lat'].mean(), lakes_in_district['Lon'].mean()], zoom_start=8)
    
    for _, lake in lakes_in_district.iterrows():
        folium.Marker(
            location=[lake['Lat'], lake['Lon']],
            popup=f"Lake ID: {lake['Lake_id']}",
            tooltip=f"Lake ID: {lake['Lake_id']}"
        ).add_to(m)

    st_folium(m, width=700, height=500)
else:
    st.warning("No lakes found in the selected district.")

# Step 4: Choose a lake from a dropdown (sorted list)
lake_ids = sorted(lakes_in_district['Lake_id'].dropna().unique())
default_lake_id = lake_ids[0] if lake_ids else None
selected_lake_id = st.sidebar.selectbox("Select a Lake ID:", lake_ids, index=lake_ids.index(default_lake_id) if default_lake_id else 0)

# Function to generate the plot
def plot_lake_data(lake_id):
    try:
        lake_data = df[df['Lake_id'] == lake_id]

        if lake_data.empty:
            st.error("No data available for the selected Lake ID.")
            return

        # Extract time-series columns (Assuming columns are in 'YYYY_MM' format)
        time_columns = [col for col in df.columns if col.endswith(('_01', '_02', '_03', '_04', '_05', '_06', 
                                                                 '_07', '_08', '_09', '_10', '_11', '_12'))]
        dates = [f"{col[:4]}-{col[5:7]}-01" for col in time_columns]  # Convert to YYYY-MM-DD format
        dates = pd.to_datetime(dates, errors='coerce')
        water_area = lake_data[time_columns].values.flatten()

        # Plot the data
        st.subheader(f'Water Area for Lake ID {lake_id} Over Time')
        plt.figure(figsize=(10, 6))
        plt.plot(dates, water_area, marker='o', label='Water Area', color='tab:blue')
        plt.xlabel('Date')
        plt.ylabel('Water Area')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        st.pyplot(plt)
    except Exception as e:
        st.error(f"Error while plotting data: {e}")

# Display time series plot for the selected lake
if selected_lake_id:
    plot_lake_data(selected_lake_id)
