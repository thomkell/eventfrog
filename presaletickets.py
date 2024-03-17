# Thomas Keller
# Eventfrog Ticket Sales over years script
# env: base

# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime


# file paths for each year
file_paths = {
    '2019': '2019.xlsx',
    '2022': '2022.xlsx',
    '2023': '2023.xlsx',
    '2024': '2024.xlsx'
}

# Create a figure
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(16, 12))

# Flatten the axis array for easier iteration
axs = axs.flatten()

# Adjust space between subplots for clarity
plt.subplots_adjust(hspace=0.5, wspace=0.3)

# Mapping years to the appropriate subplot index
year_to_subplot_index = {
    '2019': 0,
    '2022': 2,
    '2023': 1,
    '2024': 3
}

# Iterate through each year and its corresponding file
for year, file_path in file_paths.items():
    ax = axs[year_to_subplot_index[year]]
    
    # Read the file
    data = pd.read_excel(file_path, usecols=['Kaufdatum'])
    # Parse dates
    data['Kaufdatum'] = pd.to_datetime(data['Kaufdatum'], dayfirst=True)
    
    # Convert dates to "day of the year" for alignment
    data['DayOfYear'] = data['Kaufdatum'].dt.dayofyear
    
    # Aggregate ticket sales by "day of the year"
    sales_by_day_of_year = data.groupby('DayOfYear').size()

    # Calculate the total number of tickets sold
    total_sold = sales_by_day_of_year.sum()

    # Plot the data with smaller markers and a smoother line
    ax.plot(sales_by_day_of_year.index, sales_by_day_of_year.values, marker='o', markersize=4, linestyle='-', linewidth=1.5)
    # Include the total sold in the title
    ax.set_title(f'Ticket Presales Per Day in {year} (Total Sold: {total_sold})', fontweight='bold')
    ax.set_xlim(15, 161)  # Limit x-axis
    ax.set_ylim(-1, 70)  # Set y-axis limits
    ax.set_ylabel('Number of Tickets Sold')
    ax.grid(True)

    # Adjusting x-axis to show specific months as markers
    ax.set_xticks(np.linspace(15, 150, 5))
    ax.set_xticklabels(['Feb', 'Mar', 'Apr', 'May', 'Jun'])

# Add a title to the figure
# fig.suptitle('Ticket Presales Per Day from January to June (2019, 2022-2024)', fontsize=16, fontweight='bold', y=1.02)

plt.savefig('Ticketsales.png')

plt.tight_layout()
plt.show()

# Cumulative sales comparison

# Get today's day of the year
today_day_of_year = datetime.now().timetuple().tm_yday

# Store cumulative sales up to today's date for each year
cumulative_sales_until_today = {}

# Repeat the data processing to calculate cumulative sales
for year, file_path in file_paths.items():
    data = pd.read_excel(file_path, usecols=['Kaufdatum'])
    data['Kaufdatum'] = pd.to_datetime(data['Kaufdatum'], dayfirst=True)
    data['DayOfYear'] = data['Kaufdatum'].dt.dayofyear
    sales_by_day_of_year = data.groupby('DayOfYear').size().cumsum()
    
    # Find the last available sale up to today's date for each year
    if today_day_of_year in sales_by_day_of_year.index:
        cumulative_sales_until_today[year] = sales_by_day_of_year[today_day_of_year]
    else:
        # If no exact match, get the closest previous value
        closest_day = sales_by_day_of_year.index[sales_by_day_of_year.index < today_day_of_year].max()
        cumulative_sales_until_today[year] = sales_by_day_of_year[closest_day]

# plot the cumulative sales until today's date for each year
plt.figure(figsize=(10, 6))
years = list(cumulative_sales_until_today.keys())
sales_values = list(cumulative_sales_until_today.values())

plt.bar(years, sales_values, color='skyblue')

plt.title('Cumulative Ticket Sales Up to Today\'s Date Each Year', fontsize=16, fontweight='bold')
plt.xlabel('Year')
plt.ylabel('Cumulative Tickets Sold')
plt.grid(axis='y')

plt.savefig('Cumulative_ticketsales.png')
plt.show()