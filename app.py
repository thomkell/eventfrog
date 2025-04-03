import streamlit as st
from eventfrog_data import get_category_sales, plot_category_sales, load_sales_data, preprocess_sales_data, aggregate_sales_timeline, plot_cumulative_sales, get_ticket_locations, geocode_locations, plot_ticket_locations, plot_tickets_sold_by_location

st.title("Eventfrog Ticket Sales Dashboard")

# File paths
path = "/Users/thomaskeller/Dropbox/RK/Eventfrog"
filepaths = {
    "2019": f"{path}/2019.xlsx",
    "2022": f"{path}/2022.xlsx",
    "2023": f"{path}/2023.xlsx",
    "2024": f"{path}/2024.xlsx",
    "2025": f"{path}/2025.xlsx"
}

# Category Sales
st.header("Sold Ticket Sales per Category (2025)")
sold_category_sales, df_sold = get_category_sales(filepaths["2025"])
fig_category_sales = plot_category_sales(sold_category_sales, df_sold)
st.plotly_chart(fig_category_sales)

# Cumulative Sales Comparison
st.header("Cumulative Ticket Pre-Sales Comparison (December - May)")
sales_data = load_sales_data(filepaths)
preprocessed_sales_data = preprocess_sales_data(sales_data)
cumulative_sales_timeline = aggregate_sales_timeline(preprocessed_sales_data)
fig_cumulative_sales = plot_cumulative_sales(cumulative_sales_timeline)
st.plotly_chart(fig_cumulative_sales)

# Ticket Sales Locations
st.header("Ticket Sales Locations")
ticket_locations = get_ticket_locations(filepaths["2025"])
cache_path = "/Users/thomaskeller/Dropbox/RK/Eventfrog/cached_locations.csv"
ticket_locations_geocoded = geocode_locations(ticket_locations, cache_path)
fig_ticket_locations = plot_ticket_locations(ticket_locations_geocoded)
st.plotly_chart(fig_ticket_locations)

# Tickets Sold by Location
st.header("Tickets Sold Per Location")
fig_tickets_sold_by_location = plot_tickets_sold_by_location(ticket_locations_geocoded)
st.plotly_chart(fig_tickets_sold_by_location)

fig = plot_cumulative_sales(cumulative_sales_timeline)
fig.write_html("dashboard.html", full_html=True)