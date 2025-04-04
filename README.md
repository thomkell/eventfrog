# 🎟️ Eventfrog Ticket Sales Analysis

This project analyzes and visualizes ticket sales data from [Eventfrog](https://eventfrog.ch), focusing on trends from January to June across multiple years (2019, 2022, 2023, 2024). The goal is to better understand customer behavior and presale performance over time.

---

## 📁 Repository Structure

| File                        | Description |
|----------------------------|-------------|
| `scripts/TicketBuyLocations.py`    | Analyzes the geographical distribution, helping to understand where ticket purchases are coming from |
| `scripts/TicketSold.py`            | Aggregates and analyzes total ticket sales per event, year, or time window. Useful for identifying peak sales periods |
| `scripts/printSalesoverAllyears.py`| Generates a year-over-year comparison of ticket presales, visualizing daily and cumulative trends between ex. January and June |
| `app.py`                   | The main Streamlit application file for the dashboard |
| `eventfrog_data.py`        | Contains data processing and plotting functions |
| `requirements.txt`         | Lists the project dependencies |

---

## 📊 Features

- Daily presales trend visualization per year
- Cumulative ticket sales comparison by year (up to current date)
- Buyer location heatmaps or summaries
- Modular scripts for independent or combined use
- Clear, presentation-ready plots for internal reporting or public updates
- Sidebar for selecting a year to view sold tickets for that specific year

---

## 🛠️ Built With

- **Streamlit** – Web framework for the dashboard
- **pandas** – Data wrangling and aggregation
- **plotly** – Interactive data visualization
- **geopandas** – Geospatial data handling
- **geopy** – Geocoding locations
- **openpyxl** – Excel file handling

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/thomkell/eventfrog.git
cd eventfrog
