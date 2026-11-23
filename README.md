# Sales Data Analysis Using Python and Pandas

**Week 3 Internship Task**

A beginner-friendly Python project that reads sales data from a CSV file, cleans it, calculates important sales numbers (like total revenue and the best-selling product) and writes a report automatically.

---

## Table of Contents

1. [Project Introduction](#1-project-introduction)
2. [Objectives](#2-objectives)
3. [Technologies Used](#3-technologies-used)
4. [Project Structure](#4-project-structure)
5. [Dataset Description](#5-dataset-description)
6. [Installation Instructions](#6-installation-instructions)
7. [How to Run the Project](#7-how-to-run-the-project)
8. [Analysis Methodology](#8-analysis-methodology)
9. [Data Cleaning Process](#9-data-cleaning-process)
10. [Metrics Calculated](#10-metrics-calculated)
11. [Testing Instructions](#11-testing-instructions)
12. [Expected Output](#12-expected-output)
13. [Conclusion](#13-conclusion)

---

## 1. Project Introduction

Every shop or company records its sales. But a long list of sales is hard to understand by just looking at it. Data analysis turns that list into useful answers, such as:

- How much money did we earn?
- Which product sells the most?
- Which product earns the most money?

In this project, we use **Python** and a library called **Pandas** to answer these questions from a sales file with products like Laptop, Mouse, Keyboard, Monitor and Headphones.

## 2. Objectives

- Load a CSV file into Python using Pandas.
- Explore the data (first rows, shape, column names, data types).
- Find and fix problems in the data (duplicate rows and missing values).
- Calculate total revenue, total units sold and average sales.
- Find the highest and lowest sale.
- Find the best-selling product.
- Show product-wise sales performance.
- Generate a report (`analysis_report.md`) automatically from the real results.
- Test the code with simple automated tests.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.9 or newer | Programming language |
| Pandas | Reading, cleaning and analysing the data |
| Pytest | Running the automated tests |
| Markdown | Writing the report and documentation |
| Git and GitHub | Version control and sharing the project |

## 4. Project Structure

```
sales-data-analysis/
├── sales_analysis.py        # Main program (all the analysis code)
├── test_sales_analysis.py   # Automated tests
├── sales_data.csv           # Dataset (100 rows, 5 columns)
├── analysis_report.md       # Report created automatically by the program
├── requirements.txt         # Python libraries needed
├── README.md                # This file
├── .gitignore               # Files Git should ignore
└── screenshots/             # Put your screenshots here
```

## 5. Dataset Description

The file `sales_data.csv` has **100 rows** and **5 columns**:

| Column | Meaning | Example |
|---|---|---|
| Date | Day of the sale (YYYY-MM-DD) | 2026-01-03 |
| Product | Product sold | Laptop |
| Quantity | Number of units sold | 3 |
| Unit_Price | Price of one unit in INR | 55000 |
| Total_Sales | Quantity x Unit_Price in INR | 165000 |

The data is **sample data** made for learning. It covers sales from January to March 2026.

On purpose, the file contains some problems so that data cleaning can be shown:

- **5 duplicate rows** (the same sale entered twice)
- **8 missing values**: 1 in Date, 2 in Quantity, 2 in Unit_Price and 3 in Total_Sales

## 6. Installation Instructions

**Step 1: Install Python.** Download it from [python.org](https://www.python.org/downloads/). To check that it works, open a terminal and type:

```bash
python --version
```

(On some computers the command is `python3` instead of `python`.)

**Step 2: Get the project.** Download the ZIP file and extract it, or clone it from GitHub. Then open a terminal inside the `sales-data-analysis` folder:

```bash
cd sales-data-analysis
```

**Step 3 (recommended): Create a virtual environment.** This keeps the project libraries separate from the rest of your computer.

```bash
# Create it
python -m venv venv

# Activate it on Windows
venv\Scripts\activate

# Activate it on macOS / Linux
source venv/bin/activate
```

**Step 4: Install the libraries.**

```bash
pip install -r requirements.txt
```

## 7. How to Run the Project

Make sure your terminal is inside the `sales-data-analysis` folder, then run:

```bash
python sales_analysis.py
```

The program prints every step on the screen and creates (or updates) the file `analysis_report.md`.

## 8. Analysis Methodology

The program works in six simple steps:

1. **Load**: Read `sales_data.csv` with `pd.read_csv()`.
2. **Explore**: Show the first 5 rows, the shape, column names, data types and missing values.
3. **Clean**: Remove duplicates and fix missing values.
4. **Calculate**: Work out the sales metrics.
5. **Summarise by product**: Group the rows by product to compare them.
6. **Report**: Write all real results into `analysis_report.md`.

The code is split into small functions (`load_data`, `explore_data`, `clean_data`, `calculate_metrics`, `generate_report`). Each function does one job, which makes the code easy to read and easy to test.

## 9. Data Cleaning Process

Real data is rarely perfect. This is how each problem is handled:

| Problem | What the program does | Why |
|---|---|---|
| Duplicate rows | Removes them with `drop_duplicates()` | The same sale should not be counted twice. |
| Missing **Date** or **Product** | Drops that row | We cannot say when or what was sold, so the row cannot be used. |
| Missing **Unit_Price** | Fills it with the **median** price of the same product | Prices of one product are similar. The median is not affected by unusual values. |
| Missing **Quantity** | Fills it with the **median** quantity of the same product | This gives a reasonable estimate without very large or very small values. |
| Missing **Total_Sales** | Recalculates it as `Quantity x Unit_Price` | Total_Sales can always be worked out from the other two columns. |

> **Note:** Filling a missing Quantity with the median is an *estimate*, not the true value. In a real company you would ask the sales team for the correct number. Here, it shows a common data-cleaning technique.

## 10. Metrics Calculated

| Metric | How it is calculated |
|---|---|
| Total revenue | Sum of all `Total_Sales` |
| Total units sold | Sum of all `Quantity` |
| Average sales | Mean of `Total_Sales` (average value of one sale) |
| Highest sale | Row with the largest `Total_Sales` |
| Lowest sale | Row with the smallest `Total_Sales` |
| Best-selling product | Product with the most units sold (sum of `Quantity`) |
| Product-wise sales | Units, revenue, average sale, number of sales and revenue share for each product |
| Best month (extra) | Month with the highest revenue |

## 11. Testing Instructions

The file `test_sales_analysis.py` checks that the project works correctly. Run it with:

```bash
pytest -v
```

The tests check that:

| Test | What it checks |
|---|---|
| `test_csv_loads_successfully` | The CSV file loads into a table |
| `test_dataset_has_100_rows` | The dataset has exactly 100 rows |
| `test_required_columns_exist` | All 5 required columns are present |
| `test_missing_values_are_handled` | The raw data has gaps, the cleaned data has none |
| `test_duplicates_are_removed` | The raw data has duplicates, the cleaned data has none |
| `test_revenue_matches_quantity_times_price` | Total revenue equals Quantity x Unit_Price added up |
| `test_calculations_on_small_example` | Results are correct on a tiny example worked out by hand |
| `test_report_is_generated` | The report file is created and contains the real results |

Expected result:

```
test_sales_analysis.py::test_csv_loads_successfully PASSED
test_sales_analysis.py::test_dataset_has_100_rows PASSED
test_sales_analysis.py::test_required_columns_exist PASSED
test_sales_analysis.py::test_missing_values_are_handled PASSED
test_sales_analysis.py::test_duplicates_are_removed PASSED
test_sales_analysis.py::test_revenue_matches_quantity_times_price PASSED
test_sales_analysis.py::test_calculations_on_small_example PASSED
test_sales_analysis.py::test_report_is_generated PASSED
============================== 8 passed in 0.30s ===============================
```

## 12. Expected Output

When you run `python sales_analysis.py`, you should see this in the terminal:

```
============================================================
STEP 1: LOADING DATA
============================================================
Loaded 100 rows from sales_data.csv

============================================================
STEP 2: DATA EXPLORATION
============================================================

First 5 rows:
         Date     Product  Quantity  Unit_Price  Total_Sales
0  2026-01-01    Keyboard       3.0      1299.0       3897.0
1  2026-01-01    Keyboard       2.0      1299.0       2598.0
2  2026-01-02  Headphones       2.0      1999.0       3998.0
3  2026-01-02    Keyboard       2.0      1899.0       3798.0
4  2026-01-02    Keyboard       2.0      1899.0       3798.0

Dataset shape: 100 rows x 5 columns

Column names:
['Date', 'Product', 'Quantity', 'Unit_Price', 'Total_Sales']

Data types:
Date               str
Product            str
Quantity       float64
Unit_Price     float64
Total_Sales    float64
dtype: object

Missing values in each column:
Date           1
Product        0
Quantity       2
Unit_Price     2
Total_Sales    3
dtype: int64

Duplicate rows: 5

============================================================
STEP 3: DATA CLEANING
============================================================
Rows before cleaning                 : 100
Duplicate rows removed               : 5
Rows dropped (missing Date/Product)  : 1
Unit_Price values filled (median)    : 2
Quantity values filled (median)      : 2
Total_Sales recalculated (Qty x Price): all 94 rows (3 were missing)
Rows after cleaning                  : 94

Missing values after cleaning:
Date           0
Product        0
Quantity       0
Unit_Price     0
Total_Sales    0
dtype: int64

============================================================
STEP 4: SALES METRICS
============================================================
Total revenue       : INR 2,371,125.00
Total units sold    : 384
Average sale        : INR 25,224.73
Highest sale        : INR 165,000.00 (3 x Laptop on 2026-01-03)
Lowest sale         : INR 599.00 (1 x Mouse on 2026-01-10)
Best-selling product: Mouse (134 units)

============================================================
STEP 5: PRODUCT-WISE SALES
============================================================
            Units_Sold    Revenue  Average_Sale  Transactions  Revenue_Share_%
Product                                                                       
Laptop              27  1511982.0     107998.71            14            63.77
Monitor             25   326975.0      27247.92            12            13.79
Headphones          91   273909.0      11412.88            24            11.55
Keyboard           107   169393.0       7058.04            24             7.14
Mouse              134    88866.0       4443.30            20             3.75

============================================================
STEP 6: REPORT
============================================================
Report saved to: analysis_report.md
```

> **Note:** If you use an older version of Pandas, the `Date` and `Product` data types may show as `object` instead of `str`. This is normal.

The program also creates **`analysis_report.md`** with the project overview, dataset description, cleaning steps, metrics, product-wise table, key insights and conclusion. All numbers in it come from the real calculations.

**Screenshots:** After running the project, take a screenshot of the terminal output and of the test results, and save them in the `screenshots/` folder.

## 13. Conclusion

This project shows the full flow of a small data analysis task: load, explore, clean, calculate and report. After cleaning, 94 of the 100 rows were used, and the results showed that **Mouse** sold the most units while **Laptop** earned the most revenue. This is a good reminder that the best-selling product by quantity is not always the product that earns the most money.

You can extend this project by adding charts with Matplotlib, analysing sales by month or week, or loading your own sales file.

---

*Created for the Week 3 internship task: Sales Data Analysis Using Python and Pandas.*
