import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
from geopy.geocoders import Nominatim
import time
import os
import certifi

def get_category_sales(file_path):
    df_2025 = pd.read_excel(file_path)
    df_sold = df_2025[(df_2025["Status"] == "verkauft") & (df_2025["Bezahlt"] == "ja")]
    sold_category_sales = df_sold["Kategorie"].value_counts().reset_index()
    sold_category_sales.columns = ['Category', 'Tickets Sold']
    return sold_category_sales, df_sold

def plot_category_sales(sold_category_sales, df_sold):
    fig = go.Figure(data=[
        go.Bar(x=sold_category_sales['Category'], y=sold_category_sales['Tickets Sold'])
    ])
    fig.update_layout(
        title=f'Sold Ticket Sales per Category (2025) - Total: {len(df_sold)}',
        xaxis_title='Category',
        yaxis_title='Number of Tickets Sold'
    )
    return fig

def load_sales_data(files):
    dfs = {}
    for year, file in files.items():
        dfs[year] = pd.read_excel(file)

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
    df_tickets = pd.read_excel(file_path, sheet_name='Tickets')
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
    if os.path.exists(cache_path):
        location_coords_df = pd.read_csv(cache_path)
        location_coords = dict(zip(location_coords_df['ort'], zip(location_coords_df['latitude'], location_coords_df['longitude'])))
    else:
        location_coords = {}

    geolocator = Nominatim(user_agent="ticket_sales_mapping", scheme='https', ssl_context=certifi.where())

    def get_coordinates(location):
        if location in location_coords:
            return location_coords[location]
        
        try:
            geo = geolocator.geocode(location + ", Switzerland", timeout=10)
            if geo:
                location_coords[location] = (geo.latitude, geo.longitude)
                return geo.latitude, geo.longitude
        except Exception as e:
            print(f"Error fetching {location}: {e}")
        
        location_coords[location] = (None, None)
        return None, None

    df[['latitude', 'longitude']] = df['ort'].apply(lambda x: pd.Series(get_coordinates(x)))
    time.sleep(1)

    updated_cache_df = pd.DataFrame([
        {'ort': loc, 'latitude': lat, 'longitude': lon}
        for loc, (lat, lon) in location_coords.items()
    ])
    updated_cache_df.to_csv(cache_path, index=False)
    return df

def plot_ticket_locations(df):
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))
    fig = px.scatter_mapbox(gdf, lat="latitude", lon="longitude", hover_name="ort", size="tickets_sold", zoom=6, mapbox_style="open-street-map", color_discrete_sequence=["red"])
    fig.update_layout(title="Ticket Sales Locations")
    return fig

def plot_tickets_sold_by_location(df):
    fig = px.bar(df, x='ort', y='tickets_sold', title='Tickets Sold Per Location')
    fig.update_layout(xaxis_title='Location', yaxis_title='Number of Tickets Sold')
    return fig
