'''
add to <head>
<title>Saint-P Secret Map</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🎯</text></svg>">
'''
import pandas as pd
from opencage.geocoder import OpenCageGeocode
import folium
from folium.plugins import MarkerCluster, LocateControl, Search
import random

# Load your CSV file and preprocess
df = pd.read_csv('addresses.csv')

# Ensure Latitude and Longitude are numeric
df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')

# Drop rows with invalid Latitude or Longitude values
df = df.dropna(subset=['Latitude', 'Longitude'])
print('finished working with df')

def random_color():
    return random.choice(['lightgray', 'beige', 'darkblue', 'orange', 'red', 'pink', 'darkred', 'lightgreen', 'darkpurple', 'blue', 'lightred', 'black', 'darkgreen', 'cadetblue', 'gray', 'green', 'lightblue', 'purple', 'white'])


# Create a map centered around an average location
map_osm = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=12)

# Add a MarkerCluster layer
marker_cluster = MarkerCluster().add_to(map_osm)


for _, row in df.iterrows():
    c = random_color()
    address = ' '.join(row['address'].split(' ')[1:])  # Remove the first word
    popup_text = f"{address}, {row['code']}"
    marker = folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=popup_text,
        icon=folium.Icon(color=c)
    )
    marker.add_to(marker_cluster)

# Add a Leaflet control for locating user's position
LocateControl().add_to(map_osm)

# Save the map as an HTML file
map_osm.save('index.html')
