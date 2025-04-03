import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

filepath = '/Users/thomaskeller/Dropbox/RK/Eventfrog'  # Define filepath globally

def get_category_sales(file_path):
    df_2025 = pd.read_excel(file_path)
    df_sold = df_2025[(df_2025["Status"] == "verkauft") & (df_2025["Bezahlt"] == "ja")]
    sold_category_sales = df_sold["Kategorie"].value_counts().reset_index()
    sold_category_sales.columns = ['Category', 'Tickets Sold']
    return sold_category_sales

def plot_category_sales(sold_category_sales):
    total_sold = sold_category_sales['Tickets Sold'].sum()

    fig = go.Figure(data=[
        go.Bar(x=sold_category_sales['Category'], y=sold_category_sales['Tickets Sold'])
    ])
    fig.update_layout(
        title=f'Sold Ticket Sales per Category (2025) — Total: {total_sold}',
        xaxis_title='Category',
        yaxis_title='Number of Tickets Sold'
    )
    return fig
