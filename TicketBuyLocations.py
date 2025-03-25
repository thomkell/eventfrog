import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from geopy.geocoders import Nominatim
import time

# Load Excel file
file_path = "/Users/thomaskeller/Dropbox/RK/Eventfrog/2025.xlsx"  # Update this path
xls = pd.ExcelFile(file_path)

# Load ticket data
df_tickets = pd.read_excel(xls, sheet_name='Tickets')

# Normalize location names to lowercase
df_tickets['ort'] = df_tickets['Ort'].str.lower()

# Aggregate ticket sales per location (case-insensitive)
df_region_counts = df_tickets['ort'].value_counts().reset_index()
df_region_counts.columns = ['ort', 'tickets_sold']

# Initialize geolocator
geolocator = Nominatim(user_agent="ticket_sales_mapping")

# Dictionary to store already-fetched coordinates (avoids duplicate API calls)
location_coords = {}

# Function to fetch coordinates only if not already retrieved
def get_coordinates(location):
    if location in location_coords:
        return location_coords[location]  # Return cached value
    
    try:
        print(f"fetching coordinates for: {location}...")  # Print progress
        geo = geolocator.geocode(location + ", Switzerland", timeout=10)
        if geo:
            print(f" → {location}: {geo.latitude}, {geo.longitude}")  # Print result
            location_coords[location] = (geo.latitude, geo.longitude)  # Cache it
            return geo.latitude, geo.longitude
    except Exception as e:
        print(f"error fetching {location}: {e}")  # Print errors
    
    location_coords[location] = (None, None)  # Cache failed lookups
    return None, None

# Fetch coordinates for each unique lowercase location (only once)
df_region_counts[['latitude', 'longitude']] = df_region_counts['ort'].apply(lambda x: pd.Series(get_coordinates(x)))
time.sleep(1)  # Delay to prevent API throttling

# Separate locations that couldn't be geocoded
df_missing = df_region_counts[df_region_counts['latitude'].isna()]
df_map = df_region_counts.dropna()  # Keep only successful geocoded locations

# ✅ Load Switzerland map from downloaded shapefile
world = gpd.read_file("~/geodata/ne_110m_admin_0_countries.shp")
switzerland = world[world["ADMIN"] == "Switzerland"]  # Filter only Switzerland

# Create a GeoDataFrame for ticket sales locations
gdf = gpd.GeoDataFrame(df_map, geometry=gpd.points_from_xy(df_map.longitude, df_map.latitude))

# ✅ **PLOT 1: MAP OF TICKET SALES**
fig, ax = plt.subplots(figsize=(10, 8))
switzerland.plot(ax=ax, color='lightgrey')

# Plot ticket sales locations, with dot size based on ticket count
gdf.plot(ax=ax, column='tickets_sold', cmap='Reds', legend=True,
         markersize=gdf['tickets_sold'] * 10, alpha=0.6, edgecolor='black')

plt.title("Ticket Sales Distribution in Switzerland", fontsize=14)
plt.xlabel("Longitude")
plt.ylabel("Latitude")

plt.show()

# ✅ **Print missing locations below the plot**
if not df_missing.empty:
    print("\n⚠️ The following locations could not be geocoded:\n")
    print(df_missing['ort'].to_string(index=False))

# ✅ **PLOT 2: BAR CHART OF TICKET SALES PER LOCATION**
fig, ax = plt.subplots(figsize=(12, 6))
df_region_counts_sorted = df_region_counts.sort_values(by="tickets_sold", ascending=False)

plt.bar(df_region_counts_sorted["ort"], df_region_counts_sorted["tickets_sold"], color="skyblue")
plt.xlabel("Location")
plt.ylabel("Number of Tickets Sold")
plt.title("Tickets Sold Per Location")
plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
plt.show()
