# Eventfrog Tickets Sales Analysis

This project contains a Python script for analyzing and visualizing the ticket sales data from Eventfrog. It compares ticket presales per day from January to June across multiple years (2019, 2022, 2023, 2024) and provides insights into the sales trends.

## Description

The Python script utilizes `pandas` for data manipulation, `matplotlib` for visualization, and `datetime` for handling date information. It creates two types of plots: individual year trends and cumulative sales comparisons up to the current date each year.

## Getting Started

### Dependencies

* Python 3.8 or higher
* Pandas library
* Matplotlib library
* OpenPyXL library (for reading Excel files if using `.xlsx`)

### Installing

* Clone this repository or download the script to your local machine.
* Ensure you have the required Excel files with sales data named as `2019.xlsx`, `2022.xlsx`, `2023.xlsx`, and `2024.xlsx` or adjsut according to your data.

### Executing the Program

To run the program, navigate to the directory containing the script and execute:

```bash
python ticket_sales_analysis.py
