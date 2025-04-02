import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from geopy.geocoders import Nominatim
import time
import os

# === 1. Load Excel file ===
file_path = "/Users/thomaskeller/Dropbox/RK/Eventfrog/2025.xlsx"
xls = pd.ExcelFile(file_path)
df_tickets = pd.read_excel(xls, sheet_name='Tickets')

# === 2. Pre-clean raw location strings ===
df_tickets['ort'] = (
    df_tickets['Ort']
    .str.lower()
    .str.replace(r"[\.]", "", regex=True)        # remove dots like in "a.a."
    .str.replace(r"\s+", " ", regex=True)        # normalize multiple spaces
    .str.strip()
)

# === 3. Preview raw values BEFORE aliasing ===
print("\n🔍 Top 100 raw location strings BEFORE alias mapping:\n")
print(df_tickets['ort'].value_counts().head(100).to_string())

# === 4. Manual corrections for known location variants ===
location_aliases = {
    "bremgarten ag": "bremgarten",
    "bremgarten (ag)": "bremgarten",
    "affoltern a a": "affoltern am albis",
    "affoltern aa": "affoltern am albis",
    "affotern a albis": "affoltern am albis",
    "affoltern am a": "affoltern am albis",
    "affoltern": "affoltern am albis",
    "rudolfstetten-friedlisberg": "rudolfstetten",
    "aarau rohr": "aarau",
    "rohr": "aarau",
    "belikon": "bellikon",
    "belligkon": "bellikon",
    "zuerich": "zurich",
    "zürich": "zurich",
    "zh": "zurich",
    "nesselbach": "zurich",
    "buttwil": "zurich",
    "mulligen": "mellingen",
    "mülligen": "mellingen",
    "planken": "planken",
    "plänken": "planken",
    "unterägeri": "unteraegeri",
    "hausern": "hausen am albis",
    "häusern": "hausen am albis",
    "oberwil-lieli": "oberwil",
    "schinzach-dorf": "schinznach",
    "arnu": "arni",
    # Add more if needed
}

df_tickets['ort'] = df_tickets['ort'].replace(location_aliases)

# === 5. Aggregate ticket sales per location ===
df_region_counts = df_tickets['ort'].value_counts().reset_index()
df_region_counts.columns = ['ort', 'tickets_sold']

# === 6. Debug: See final cleaned location values ===
print("\n📊 Cleaned location values (after alias mapping):\n")
print(df_region_counts['ort'].value_counts().to_string())

# === 7. Load cached coordinates if available ===
cache_path = "/Users/thomaskeller/Dropbox/RK/Eventfrog/cached_locations.csv"
if os.path.exists(cache_path):
    location_coords_df = pd.read_csv(cache_path)
    location_coords = dict(zip(location_coords_df['ort'], zip(location_coords_df['latitude'], location_coords_df['longitude'])))
else:
    location_coords = {}

# === 8. Set up geolocator ===
geolocator = Nominatim(user_agent="ticket_sales_mapping")

# === 9. Geocode with caching ===
def get_coordinates(location):
    if location in location_coords:
        return location_coords[location]
    
    try:
        print(f"Fetching coordinates for: {location}...")
        geo = geolocator.geocode(location + ", Switzerland", timeout=10)
        if geo:
            print(f" → {location}: {geo.latitude}, {geo.longitude}")
            location_coords[location] = (geo.latitude, geo.longitude)
            return geo.latitude, geo.longitude
    except Exception as e:
        print(f"Error fetching {location}: {e}")
    
    location_coords[location] = (None, None)
    return None, None

# === 10. Fetch coordinates for cleaned locations ===
df_region_counts[['latitude', 'longitude']] = df_region_counts['ort'].apply(lambda x: pd.Series(get_coordinates(x)))
time.sleep(1)

# === 11. Separate valid / invalid geocodes ===
df_missing = df_region_counts[df_region_counts['latitude'].isna()]
df_map = df_region_counts.dropna()

# === 12. Load Switzerland shapefile ===
world = gpd.read_file("~/geodata/ne_110m_admin_0_countries.shp")
switzerland = world[world["ADMIN"] == "Switzerland"]

# === 13. GeoDataFrame for plotting ===
gdf = gpd.GeoDataFrame(df_map, geometry=gpd.points_from_xy(df_map.longitude, df_map.latitude))

# === 14. Plot: Ticket sales on map ===
fig, ax = plt.subplots(figsize=(10, 8))
switzerland.plot(ax=ax, color='lightgrey')
gdf.plot(ax=ax, column='tickets_sold', cmap='Reds', legend=True,
         markersize=gdf['tickets_sold'] * 10, alpha=0.6, edgecolor='black')
plt.title("Ticket Sales Distribution in Switzerland", fontsize=14)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()

# === 15. Print missing geocoded locations ===
if not df_missing.empty:
    print("\n⚠️ The following locations could not be geocoded:\n")
    print(df_missing['ort'].to_string(index=False))

# === 16. Plot: Bar chart ===
fig, ax = plt.subplots(figsize=(12, 6))
df_region_counts_sorted = df_region_counts.sort_values(by="tickets_sold", ascending=False)

plt.bar(df_region_counts_sorted["ort"], df_region_counts_sorted["tickets_sold"], color="skyblue")
plt.xlabel("Location")
plt.ylabel("Number of Tickets Sold")
plt.title("Tickets Sold Per Location")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# === 17. Save updated coordinates ===
updated_cache_df = pd.DataFrame([
    {'ort': loc, 'latitude': lat, 'longitude': lon}
    for loc, (lat, lon) in location_coords.items()
])
updated_cache_df.to_csv(cache_path, index=False)
print(f"\n✅ Saved coordinates to: {cache_path}")
