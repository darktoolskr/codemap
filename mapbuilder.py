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
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

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
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"{row['code']}",
        icon=folium.Icon(color=random_color())
    ).add_to(map_osm)

'''
# Add a Leaflet plugin for map rotation on touch devices
MarkerCluster().add_to(map_osm)

# Add the Leaflet.Rotate plugin
folium.TileLayer(
    tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    attr='OpenStreetMap',
    overlay=True,
    control=True,
    rotate=True
).add_to(map_osm)
'''

# Add a Leaflet control for locating user's position
LocateControl().add_to(map_osm)

# Save the map as an HTML file
map_osm.save('index.html')


# Read the saved map HTML content
with open('index.html', 'r') as file:
    map_html_content = file.read()

# Find the map variable name
import re
map_var_name_match = re.search(r'var (\w+) = L\.map\(', map_html_content)
map_var_name = map_var_name_match.group(1) if map_var_name_match else 'map'


# JavaScript for map rotation functionality
rotation_js = f"""
<script>
    var mapElement = document.getElementById('map');
    var rotationAngle = 0;

    function rotateMapLeft() {{
        rotationAngle = (rotationAngle - 15) % 360;
        mapElement.style.transform = 'rotate(' + rotationAngle + 'deg)';
    }}

    function rotateMapRight() {{
        rotationAngle = (rotationAngle + 15) % 360;
        mapElement.style.transform = 'rotate(' + rotationAngle + 'deg)';
    }}

    var startAngle, initialRotationAngle;

    function onTouchStart(event) {{
        if (event.touches.length === 2) {{
            var touch1 = event.touches[0];
            var touch2 = event.touches[1];
            startAngle = Math.atan2(touch2.pageY - touch1.pageY, touch2.pageX - touch1.pageX) * 180 / Math.PI;
            initialRotationAngle = rotationAngle;
        }}
    }}

    function onTouchMove(event) {{
        if (event.touches.length === 2) {{
            var touch1 = event.touches[0];
            var touch2 = event.touches[1];
            var currentAngle = Math.atan2(touch2.pageY - touch1.pageY, touch2.pageX - touch1.pageX) * 180 / Math.PI;
            rotationAngle = initialRotationAngle + (currentAngle - startAngle);
            mapElement.style.transform = 'rotate(' + rotationAngle + 'deg)';
        }}
    }}

    document.addEventListener('touchstart', onTouchStart, false);
    document.addEventListener('touchmove', onTouchMove, false);
</script>
"""

# Add rotation buttons to the HTML
rotation_buttons_html = """
<div style="position: absolute; top: 10px; left: 10px; z-index: 1000;">
    <button onclick="rotateMapLeft()">Rotate Left</button>
    <button onclick="rotateMapRight()">Rotate Right</button>
</div>
"""

# Insert the rotation buttons and JavaScript into the map HTML content
final_html_content = map_html_content.replace(
    '<body>', f'<body>{rotation_buttons_html}'
)
final_html_content = final_html_content.replace(
    '</body>', rotation_js + '</body>'
)

# Add CSS to make the map fullscreen and adjust its transformation origin
css_style = """
<style>
    #map {
        width: 100vw;
        height: 100vh;
        transform-origin: center center;
        position: absolute;
        top: 0;
        left: 0;
    }
    html, body {
        margin: 0;
        padding: 0;
        height: 100%;
        overflow: hidden;
    }
</style>
"""

final_html_content = final_html_content.replace('</head>', css_style + '</head>')

# Save the complete HTML file with rotation functionality
with open('index.html', 'w') as file:
    file.write(final_html_content)
