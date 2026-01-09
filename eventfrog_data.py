import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
from geopy.geocoders import Nominatim
import time
import os
import certifi
import ssl

def find_header_row(file_path, sheet_name=0):
    """Find the row where actual header data starts by looking for common column names"""
    try:
        df_raw = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
        # Look for rows that contain common header keywords
        for idx, row in df_raw.iterrows():
            row_str = str(row).lower()
            if 'status' in row_str or 'kategorie' in row_str or 'preis' in row_str:
                return idx
        return 0
    except:
        return 0

def get_category_sales(file_path):
    skiprows = find_header_row(file_path)
    df = pd.read_excel(file_path, skiprows=skiprows)
    df_sold = df[(df["Status"] == "verkauft") & (df["Bezahlt"] == "ja")]
    df_sold['Category_Price'] = df_sold['Kategorie'] + ' (' + df_sold['Preis'].astype(str) + ' CHF)'
    sold_category_sales = df_sold["Category_Price"].value_counts().reset_index()
    sold_category_sales.columns = ['Category_Price', 'Tickets Sold']
    return sold_category_sales, df_sold

def plot_category_sales(sold_category_sales, df_sold):
    fig = go.Figure(data=[
        go.Bar(
            x=sold_category_sales['Category_Price'],
            y=sold_category_sales['Tickets Sold'],
            text=sold_category_sales['Tickets Sold'],
            textposition='outside'
        )
    ])

    # Give some headroom above the tallest bar so the outside text label isn't clipped
    max_tickets = sold_category_sales['Tickets Sold'].max() if not sold_category_sales.empty else 0
    y_max = max(10, max_tickets * 1.2)

    fig.update_traces(textfont_size=12)
    fig.update_layout(
        title=f'Sold Ticket Sales per Category (2025) - Total: {len(df_sold)}',
        xaxis_title='Category (Price in CHF)',
        yaxis=dict(title='Number of Tickets Sold', range=[0, y_max], automargin=True),
        margin=dict(t=110, b=80, l=60, r=40),
    )
    return fig

def load_sales_data(files):
    dfs = {}
    for year, file in files.items():
        skiprows = find_header_row(file)
        dfs[year] = pd.read_excel(file, skiprows=skiprows)

    all_data = []
    for year, df in dfs.items():
        df["Jahr"] = int(year)
        df["Kaufdatum"] = pd.to_datetime(df["Kaufdatum"], dayfirst=True)
        all_data.append(df)

    sales_data = pd.concat(all_data, ignore_index=True)
    return sales_data

def preprocess_sales_data(sales_data):
    sales_data["Month-Day"] = sales_data["Kaufdatum"].dt.strftime("%m-%d")
    sales_data = sales_data[sales_data["Kaufdatum"].dt.month.isin([12, 1, 2, 3, 4, 5, 6])]
    return sales_data

def aggregate_sales_timeline(sales_data):
    sales_timeline = sales_data.groupby(["Jahr", "Month-Day"]).size().unstack(level=0)
    sales_timeline.index = pd.to_datetime("2021-" + sales_timeline.index)
    sales_timeline.index = sales_timeline.index.map(lambda x: x if x.month != 12 else x.replace(year=2020))
    sales_timeline = sales_timeline.sort_index()
    cumulative_sales_timeline = sales_timeline.cumsum()
    return cumulative_sales_timeline

def plot_cumulative_sales(cumulative_sales_timeline):
    fig = go.Figure()
    for year in cumulative_sales_timeline.columns:
        fig.add_trace(go.Scatter(
            x=cumulative_sales_timeline.index,
            y=cumulative_sales_timeline[year],
            mode='lines+markers',
            name=str(year)
        ))

    fig.update_layout(
        title='Cumulative Ticket Sales Comparison (December - June)',
        xaxis_title='Month-Day',
        yaxis_title='Cumulative Tickets Sold',
        xaxis=dict(
            tickformat='%b %d',  # Show as 'Dec 01', 'Jan 15', etc.
            tickangle=45
        )
    )
    return fig

def get_ticket_locations(file_path):
    skiprows = find_header_row(file_path, sheet_name='Tickets')
    df_tickets = pd.read_excel(file_path, sheet_name='Tickets', skiprows=skiprows)
    df_tickets['ort'] = (
        df_tickets['Ort']
        .str.lower()
        .str.replace(r"[\.]", "", regex=True)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )
    location_aliases = {
        "bremgarten": "bremgarten ag",
        "bremgarten (ag)": "bremgarten ag",
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
        "oberwil-lieli": "lieli",
        "oberwil": "lieli",
        "schinzach-dorf": "schinznach",
        "arnu": "arni ag",
        "arni": "arni ag",
        "muri": "muri ag",
    }
    df_tickets['ort'] = df_tickets['ort'].replace(location_aliases)
    df_region_counts = df_tickets['ort'].value_counts().reset_index()
    df_region_counts.columns = ['ort', 'tickets_sold']
    return df_region_counts

def geocode_locations(df, cache_path):
    # Load existing cache
    location_coords = {}
    if os.path.exists(cache_path):
        location_coords_df = pd.read_csv(cache_path)
        for _, row in location_coords_df.iterrows():
            lat = row['latitude'] if pd.notna(row['latitude']) and row['latitude'] != '' else None
            lon = row['longitude'] if pd.notna(row['longitude']) and row['longitude'] != '' else None
            location_coords[row['ort']] = (lat, lon)

    # Create directory if needed
    cache_dir = os.path.dirname(cache_path)
    if cache_dir and not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    # Set up geolocator with proper SSL context
    try:
        ctx = ssl.create_default_context(cafile=certifi.where())
        geolocator = Nominatim(user_agent="eventfrog_ticket_analysis", timeout=10, ssl_context=ctx)
    except:
        geolocator = Nominatim(user_agent="eventfrog_ticket_analysis", timeout=10)

    locations_to_geocode = df[df['ort'].notna()]['ort'].unique()
    print(f"Processing {len(locations_to_geocode)} unique locations...")

    for location in locations_to_geocode:
        if location not in location_coords or (location_coords[location][0] is None and location_coords[location][1] is None):
            # Need to geocode this location
            try:
                time.sleep(1.5)  # Rate limiting for Nominatim
                print(f"Geocoding: {location}...", end=" ")
                geo = geolocator.geocode(location + ", Switzerland", timeout=10)
                if geo:
                    location_coords[location] = (geo.latitude, geo.longitude)
                    print(f"✓ ({geo.latitude}, {geo.longitude})")
                else:
                    print(f"✗ No results")
                    location_coords[location] = (None, None)
            except Exception as e:
                print(f"✗ Error: {e}")
                location_coords[location] = (None, None)
    
    # Apply coordinates to dataframe
    df['latitude'] = df['ort'].map(lambda x: location_coords.get(x, (None, None))[0])
    df['longitude'] = df['ort'].map(lambda x: location_coords.get(x, (None, None))[1])

    # Save cache
    updated_cache_df = pd.DataFrame([
        {'ort': loc, 'latitude': lat, 'longitude': lon}
        for loc, (lat, lon) in location_coords.items()
    ])
    updated_cache_df.to_csv(cache_path, index=False)
    print(f"✓ Cache saved to {cache_path}")
    
    # Filter to only valid coordinates for the map
    df_valid = df.dropna(subset=['latitude', 'longitude'])
    print(f"✓ {len(df_valid)}/{len(df)} locations have coordinates")
    
    return df_valid

def plot_ticket_locations(df):
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))
    fig = px.scatter_mapbox(gdf, lat="latitude", lon="longitude", hover_name="ort", size="tickets_sold", zoom=6, mapbox_style="open-street-map", color_discrete_sequence=["red"])
    fig.update_layout(title="Ticket Sales Locations")
    return fig

def plot_tickets_sold_by_location(df):
    fig = px.bar(df, x='ort', y='tickets_sold', title='Tickets Sold Per Location')
    fig.update_layout(xaxis_title='Location', yaxis_title='Number of Tickets Sold')
    return fig
