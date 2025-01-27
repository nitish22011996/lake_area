import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV data (uploaded file)
file_path = '/mnt/data/image.png'  # path to your newly uploaded file
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

# Extract the monthly data (you could choose another parameter such as trends)
dates = pd.to_datetime([col for col in time_columns])

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

