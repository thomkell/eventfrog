import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
file_path = "/Users/thomaskeller/Dropbox/RK/Eventfrog/2025.xlsx"
df_2025 = pd.read_excel(file_path)

# Filter only sold and paid tickets
df_sold = df_2025[(df_2025["Status"] == "verkauft") & (df_2025["Bezahlt"] == "ja")]

# Count the number of sold tickets per category
sold_category_sales = df_sold["Kategorie"].value_counts()

# Plot ticket sales per category (only sold/paid tickets) with value labels
plt.figure(figsize=(10, 6))
ax = sold_category_sales.plot(kind="bar", color="skyblue", edgecolor="black")

plt.title(f"Sold Ticket Sales per Category (2025) - Total: {len(df_sold)}")
plt.xlabel("Category")
plt.ylabel("Number of Tickets Sold")
plt.xticks(rotation=45)

# Add value labels on top of the bars
for bar in ax.patches:
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), 
             int(bar.get_height()), ha="center", va="bottom", fontsize=10, fontweight="bold")

plt.grid(axis="y")
plt.show()
