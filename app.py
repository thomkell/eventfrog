import streamlit as st
from eventfrog_data import get_category_sales, plot_category_sales

st.title("Eventfrog Ticket Sales Dashboard")

filepath = '/Users/thomaskeller/Dropbox/RK/Eventfrog/2025.xlsx'  # Define the file path for 2025 data

# Category Sales
sold_category_sales = get_category_sales(filepath)
fig_category_sales = plot_category_sales(sold_category_sales)

st.plotly_chart(fig_category_sales)