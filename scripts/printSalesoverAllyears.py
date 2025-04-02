import pandas as pd
import matplotlib.pyplot as plt

filepath = '/Users/thomaskeller/Dropbox/RK/Eventfrog'

# File paths
files = {
    "2022": f"{filepath}/2022.xlsx",
    "2023": f"{filepath}/2023.xlsx",
    "2024": f"{filepath}/2024.xlsx",
    "2025": f"{filepath}/2025.xlsx",
}

# Load all Excel files into separate dataframes
dfs = {}
for year, file in files.items():
    dfs[year] = pd.read_excel(file)

# Combine all years into a single DataFrame with a new column for the year
all_data = []
for year, df in dfs.items():
    df["Jahr"] = int(year)  # Add year column
    df["Kaufdatum"] = pd.to_datetime(df["Kaufdatum"], dayfirst=True)  # Convert to datetime
    all_data.append(df)

# Concatenate all years into one DataFrame
sales_data = pd.concat(all_data, ignore_index=True)

# Extract month-day format to align across years
sales_data["Month-Day"] = sales_data["Kaufdatum"].dt.strftime("%m-%d")

# Select only December to May data
sales_data = sales_data[sales_data["Kaufdatum"].dt.month.isin([12, 1, 2, 3, 4, 5])]

# Aggregate sales per day across years
sales_timeline = sales_data.groupby(["Jahr", "Month-Day"]).size().unstack(level=0)

# Convert index to datetime for correct chronological order
sales_timeline.index = pd.to_datetime("2021-" + sales_timeline.index)  # Use a reference year

# Adjust December dates to be earlier in the sequence
sales_timeline.index = sales_timeline.index.map(lambda x: x if x.month != 12 else x.replace(year=2020))

# Sort index to ensure correct order from December to May
sales_timeline = sales_timeline.sort_index()

# Compute cumulative ticket sales per day for each year
cumulative_sales_timeline = sales_timeline.cumsum()

# Plot cumulative ticket sales
plt.figure(figsize=(12, 6))
for year in cumulative_sales_timeline.columns:
    plt.plot(cumulative_sales_timeline.index, cumulative_sales_timeline[year], marker="o", label=f"{year}")

plt.title("Cumulative Ticket Sales Comparison (December - May)")
plt.xlabel("Month")
plt.ylabel("Cumulative Tickets Sold")
plt.legend(title="Year")

# Format x-axis to show only month names
plt.xticks(cumulative_sales_timeline.index.to_period("M").drop_duplicates().to_timestamp(), 
           cumulative_sales_timeline.index.strftime("%b").drop_duplicates())

plt.grid()
plt.show()
