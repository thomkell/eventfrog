import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import pandas as pd
import matplotlib.pyplot as plt

filepath = '/Users/thomaskeller/Dropbox/RK/Eventfrog'  # Define filepath globally

def get_category_sales(file_path):
    df_2025 = pd.read_excel(file_path)
    df_sold = df_2025[(df_2025["Status"] == "verkauft") & (df_2025["Bezahlt"] == "ja")]
    sold_category_sales = df_sold["Kategorie"].value_counts()
    return sold_category_sales

def plot_category_sales(sold_category_sales):
    plt.figure(figsize=(10, 6))
    ax = sold_category_sales.plot(kind="bar", color="skyblue", edgecolor="black")

    plt.title(f"Sold Ticket Sales per Category (2025) - Total: {sold_category_sales.sum()}")
    plt.xlabel("Category")
    plt.ylabel("Number of Tickets Sold")
    plt.xticks(rotation=45)

    for bar in ax.patches:
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                 int(bar.get_height()), ha="center", va="bottom", fontsize=10, fontweight="bold")

    plt.grid(axis="y")
    return plt
