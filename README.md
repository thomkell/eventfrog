# 🎟️ Eventfrog Ticket Sales Analysis

This project analyzes and visualizes ticket sales data from [Eventfrog](https://eventfrog.ch), focusing on trends from January to June across multiple years (2019, 2022, 2023, 2024). The goal is to better understand customer behavior and presale performance over time.

---

## 📁 Repository Structure

| File                        | Description |
|----------------------------|-------------|
| `TicketBuyLocations.py`    | Analyzes the geographical distribution of buyers, helping to understand where ticket purchases are coming from. |
| `TicketSold.py`            | Aggregates and analyzes total ticket sales per event, year, or time window. Useful for identifying peak sales periods. |
| `printSalesoverAllyears.py`| Generates a year-over-year comparison of ticket presales, visualizing daily and cumulative trends between January and June. |

---

## 📊 Features

- Daily presales trend visualization per year
- Cumulative ticket sales comparison by year (up to current date)
- Buyer location heatmaps or summaries
- Modular scripts for independent or combined use
- Clear, presentation-ready plots for internal reporting or public updates

---

## 🛠️ Built With

- **pandas** – Data wrangling and aggregation
- **matplotlib** – Static data visualization
- **datetime** – Temporal alignment across multiple years

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/thomkell/eventfrog.git
