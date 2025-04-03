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
    fig = go.Figure(data=[
        go.Bar(x=sold_category_sales['Category'], y=sold_category_sales['Tickets Sold'])
    ])
    fig.update_layout(
        title='Sold Ticket Sales per Category (2025)',
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
    sales_data = sales_data[sales_data["Kaufdatum"].dt.month.isin([12, 1, 2, 3, 4, 5])]
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
        title='Cumulative Ticket Sales Comparison (December - May)',
        xaxis_title='Date',
        yaxis_title='Cumulative Tickets Sold',
        xaxis=dict(
            tickformat='%b %d',  # Formats as 'Jan 01', 'Feb 15', etc.
            tickangle=45
        )
    )
    return fig