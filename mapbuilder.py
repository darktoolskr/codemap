import pandas as pd
from opencage.geocoder import OpenCageGeocode
import folium
from folium.plugins import MarkerCluster
from folium.plugins import LocateControl
import random

# Load your CSV file and preprocess
df = pd.read_csv('addresses.csv')

# Initialize OpenCage geocoder with your API key
key = '781b89ffc5eb47ab8e1b849822beacf1'
geocoder = OpenCageGeocode(key)

def random_color():
    return random.choice(['lightgray', 'beige', 'darkblue', 'orange', 'red', 'pink', 'darkred', 'lightgreen', 'darkpurple', 'blue', 'lightred', 'black', 'darkgreen', 'cadetblue', 'gray', 'green', 'lightblue', 'purple', 'white'])


def get_lat_long(address):
    result = geocoder.geocode(address)
    if result:
        return result[0]['geometry']['lat'], result[0]['geometry']['lng']
    return None, None

# Apply the function to your DataFrame
df['Latitude'], df['Longitude'] = zip(*df['address'].apply(get_lat_long))

# Save the updated DataFrame to a new CSV (if needed)
df.to_csv('updated_addresses.csv', index=False)

# Create a map centered around an average location
map_osm = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=12)

# Add markers to the map
for _, row in df.iterrows():
    c = random_color()
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"{row['code']}",
        icon=folium.Icon(color=c)
    ).add_to(map_osm)

# Add a Leaflet control for locating user's position
LocateControl().add_to(map_osm)

# Save the map as an HTML file
map_osm.save('index.html')
