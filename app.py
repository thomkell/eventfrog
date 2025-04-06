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

# Sidebar for year selection
st.sidebar.title("Select Year")
selected_year = st.sidebar.selectbox("Year", list(filepaths.keys()))

# Tabs for different plots
tab1, tab2, tab3, tab4 = st.tabs(["Sold Tickets per Category", "Cumulative Sales Comparison", "Ticket Sales Locations", "Tickets Sold Per Location"])

with tab1:
    st.header(f"Sold Ticket Sales per Category ({selected_year})")
    sold_category_sales, df_sold = get_category_sales(filepaths[selected_year])
    fig_category_sales = plot_category_sales(sold_category_sales, df_sold)
    st.plotly_chart(fig_category_sales)

with tab2:
    st.header("Cumulative Ticket Pre-Sales Comparison (December - June)")
    sales_data = load_sales_data(filepaths)
    preprocessed_sales_data = preprocess_sales_data(sales_data)
    cumulative_sales_timeline = aggregate_sales_timeline(preprocessed_sales_data)
    fig_cumulative_sales = plot_cumulative_sales(cumulative_sales_timeline)
    st.plotly_chart(fig_cumulative_sales)

with tab3:
    st.header("Ticket Sales Locations")
    ticket_locations = get_ticket_locations(filepaths[selected_year])
    cache_path = "/Users/thomaskeller/Dropbox/RK/Eventfrog/cached_locations.csv"
    ticket_locations_geocoded = geocode_locations(ticket_locations, cache_path)
    fig_ticket_locations = plot_ticket_locations(ticket_locations_geocoded)
    st.plotly_chart(fig_ticket_locations)

with tab4:
    st.header("Tickets Sold Per Location")
    fig_tickets_sold_by_location = plot_tickets_sold_by_location(ticket_locations_geocoded)
    st.plotly_chart(fig_tickets_sold_by_location)
