import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import streamlit.components.v1 as components

# Load the CSV data
df = pd.read_csv("dat.csv")

# App title
st.title('Interactive Lake Map')

# Create a leafmap map
m = leafmap.Map()

# Dropdown to select the column for filtering
option = st.selectbox(
    'Select the column to filter by:',
    ('ID', 'Climate _Zone')
)
#  'Lake_Class', 'Average Increase in temperature', 'P value'
# Check if the selected option is 'ID' or another that requires specific value input
if option == 'ID':
    # Text input for specific value
    value = st.number_input('Enter the value:', step=1)
    filtered_df = df[df[option] == value]
elif option == 'Lake_Class':
    # Get unique clarity levels
    clarity_levels = df['Lake_Class'].unique()
    # Select the clarity level
    clarity_level = st.selectbox('Select clarity level:', clarity_levels)
    filtered_df = df[df[option].str.strip() == clarity_level]  # Remove leading/trailing whitespaces before comparison
else:
    # Number input for min and max values
    min_value = st.number_input('Minimum value:', step=0.01)
    max_value = st.number_input('Maximum value:', step=0.01)
    filtered_df = df[(df[option] >= min_value) & (df[option] <= max_value)]

# Display filtered lake information
if not filtered_df.empty:
    st.write(filtered_df)

    # Add markers for all filtered lakes to the map
    for idx, row in filtered_df.iterrows():
        m.add_marker(location=(row['MEAN_Y'], row['MEAN_X']), popup=f"{option}: {row[option]}")
    st.success("Map updated with selected filters.")
else:
    st.error("No data matches your filter!")

# Display the map
map_path = "map.html"
m.to_html(outfile=map_path)
HtmlFile = open(map_path, 'r', encoding='utf-8')
source_code = HtmlFile.read() 
components.html(source_code, height=600)
