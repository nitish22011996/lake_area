import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# Load the CSV data
file_path = 'Area_f_2.csv'  # Update this with your file path
df = pd.read_csv(file_path)

# App title
st.title('Lake Monitoring - Interactive Map & Trends')

# Allow the user to enter the Lake ID manually
lake_id_input = st.text_input('Enter Lake ID (or click on a lake marker):')

# Create a map centered around the mean latitude and longitude of all lakes
m = folium.Map(location=[df['Lat'].mean(), df['Lon'].mean()], zoom_start=6)

# Add a marker cluster for better visualization
marker_cluster = MarkerCluster().add_to(m)

# Add lake markers to the map
for _, row in df.iterrows():
    folium.Marker(
        location=[row['Lat'], row['Lon']],
        popup=f"Lake ID: {row['Lake_id']}",
        tooltip="Click for details"
    ).add_to(marker_cluster)

# Display the map in Streamlit and capture the click event
st.subheader('Interactive Map of Lakes')
clicked_data = st_folium(m, width=700, height=500)

# Check if a marker was clicked
if clicked_data and clicked_data.get("last_object_clicked"):
    lake_id_clicked = clicked_data["last_object_clicked"]["popup"].split(": ")[1]
    st.write(f"Lake ID selected via map: {lake_id_clicked}")
    lake_id_input = lake_id_clicked

# Filter the dataframe by the selected or entered Lake ID
if lake_id_input:
    if lake_id_input in df['Lake_id'].astype(str).values:
        lake_data = df[df['Lake_id'].astype(str) == lake_id_input]

        # Display filtered lake information
        st.write(f"Data for Lake ID: {lake_id_input}")
        st.write(lake_data)

        # Extract the columns for the monthly data
        time_columns = [col for col in df.columns if col.endswith(('_01', '_02', '_03', '_04', '_05', '_06', '_07', '_08', '_09', '_10', '_11', '_12'))]
        lake_data[time_columns] = lake_data[time_columns].apply(pd.to_numeric, errors='coerce')

        # Plot the Water Area over Time for the selected lake
        st.subheader(f'Water Area for Lake ID {lake_id_input} Over Time')
        dates = pd.to_datetime([f"{col[:4]}-{col[5:7]}-01" for col in time_columns], errors='coerce')
        water_area = lake_data[time_columns].values.flatten()

        plt.figure(figsize=(10, 6))
        plt.plot(dates, water_area, marker='o', label='Water Area', color='tab:blue')
        plt.title(f"Water Area for Lake ID {lake_id_input} Over Time")
        plt.xlabel('Date')
        plt.ylabel('Water Area')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        st.pyplot(plt)
    else:
        st.error("Invalid Lake ID entered or selected. Please try again.")

