import streamlit as st
from eventfrog_data import get_category_sales, plot_category_sales, load_sales_data, preprocess_sales_data, aggregate_sales_timeline, plot_cumulative_sales

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
sold_category_sales = get_category_sales(filepaths["2025"])
fig_category_sales = plot_category_sales(sold_category_sales)
st.plotly_chart(fig_category_sales)

# Cumulative Sales Comparison
st.header("Cumulative Ticket Sales Comparison (December - May)")
sales_data = load_sales_data(filepaths)
preprocessed_sales_data = preprocess_sales_data(sales_data)
cumulative_sales_timeline = aggregate_sales_timeline(preprocessed_sales_data)
fig_cumulative_sales = plot_cumulative_sales(cumulative_sales_timeline)
st.plotly_chart(fig_cumulative_sales)
