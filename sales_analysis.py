"""
Sales Data Analysis Using Python and Pandas
===========================================
Week 3 Internship Task

What this script does:
    1. Loads sales data from sales_data.csv
    2. Explores the data (first rows, shape, column names, data types, missing values)
    3. Cleans the data (removes duplicates, handles missing values)
    4. Calculates sales metrics (revenue, units sold, average, highest/lowest, best seller)
    5. Prints product-wise performance
    6. Writes a Markdown report (analysis_report.md) using the real calculated results

How to run:
    python sales_analysis.py
"""

from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
# Paths are built from the location of this file, so the script works
# no matter which folder you run it from.
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "sales_data.csv"
REPORT_FILE = BASE_DIR / "analysis_report.md"

# The columns every sales file must have.
REQUIRED_COLUMNS = ["Date", "Product", "Quantity", "Unit_Price", "Total_Sales"]

# Currency label used in the console output and the report.
CURRENCY = "INR"


def money(value):
    """Format a number as money, e.g. 1234.5 -> 'INR 1,234.50'."""
    return f"{CURRENCY} {value:,.2f}"


def print_section(title):
    """Print a clear heading in the console."""
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


# ---------------------------------------------------------------------------
# Step 1: Load the data
# ---------------------------------------------------------------------------
def load_data(file_path=DATA_FILE):
    """Read the CSV file into a Pandas DataFrame."""
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Could not find the data file: {file_path}")

    # pd.read_csv() reads a CSV file and returns a DataFrame (a table).
    df = pd.read_csv(file_path)

    # Make sure all the columns we need are present.
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"The CSV file is missing these columns: {missing_columns}")

    return df


# ---------------------------------------------------------------------------
# Step 2: Explore the data
# ---------------------------------------------------------------------------
def explore_data(df):
    """Print a quick overview of the raw data."""
    print_section("STEP 2: DATA EXPLORATION")

    print("\nFirst 5 rows:")
    print(df.head())  # head() shows the first 5 rows by default

    print(f"\nDataset shape: {df.shape[0]} rows x {df.shape[1]} columns")

    print("\nColumn names:")
    print(list(df.columns))

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values in each column:")
    print(df.isnull().sum())  # isnull() marks empty cells, sum() counts them

    print(f"\nDuplicate rows: {df.duplicated().sum()}")


# ---------------------------------------------------------------------------
# Step 3: Clean the data
# ---------------------------------------------------------------------------
def clean_data(df):
    """
    Clean the raw data and return (clean_df, log).

    `log` is a dictionary that records what was changed, so the numbers
    can be shown in the console and written into the report.
    """
    df = df.copy()  # work on a copy so the original data stays untouched
    log = {
        "raw_rows": len(df),
        "raw_columns": df.shape[1],
        "missing_before": {col: int(n) for col, n in df.isnull().sum().items()},
    }

    # 3.1 Remove duplicate rows (rows that are exactly the same).
    log["duplicates_removed"] = int(df.duplicated().sum())
    df = df.drop_duplicates().reset_index(drop=True)

    # 3.2 Convert the Date column from text to real dates.
    # errors="coerce" turns invalid or empty dates into NaT (missing date).
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # 3.3 A sale without a Date or Product cannot be analysed, so drop it.
    rows_before = len(df)
    df = df.dropna(subset=["Date", "Product"]).reset_index(drop=True)
    log["rows_dropped_missing_date_or_product"] = rows_before - len(df)

    # 3.4 Fill missing Unit_Price with the median price of the same product.
    log["unit_price_filled"] = int(df["Unit_Price"].isnull().sum())
    median_price = df.groupby("Product")["Unit_Price"].transform("median")
    df["Unit_Price"] = df["Unit_Price"].fillna(median_price)

    # 3.5 Fill missing Quantity with the median quantity of the same product.
    log["quantity_filled"] = int(df["Quantity"].isnull().sum())
    median_quantity = df.groupby("Product")["Quantity"].transform("median")
    df["Quantity"] = df["Quantity"].fillna(median_quantity.round())

    # Safety net: drop any row that still has no Quantity or Unit_Price.
    rows_before = len(df)
    df = df.dropna(subset=["Quantity", "Unit_Price"]).reset_index(drop=True)
    log["rows_dropped_unfillable"] = rows_before - len(df)
    df["Quantity"] = df["Quantity"].astype(int)

    # 3.6 Calculate Total_Sales = Quantity x Unit_Price for every row.
    # This also fills the Total_Sales values that were missing.
    log["total_sales_missing"] = int(df["Total_Sales"].isnull().sum())
    df["Total_Sales"] = (df["Quantity"] * df["Unit_Price"]).round(2)

    log["rows_after"] = len(df)
    return df, log


def print_cleaning_summary(clean_df, log):
    """Show what the cleaning step did."""
    print_section("STEP 3: DATA CLEANING")
    print(f"Rows before cleaning                 : {log['raw_rows']}")
    print(f"Duplicate rows removed               : {log['duplicates_removed']}")
    print(f"Rows dropped (missing Date/Product)  : {log['rows_dropped_missing_date_or_product']}")
    print(f"Unit_Price values filled (median)    : {log['unit_price_filled']}")
    print(f"Quantity values filled (median)      : {log['quantity_filled']}")
    print(f"Total_Sales recalculated (Qty x Price): all {log['rows_after']} rows "
          f"({log['total_sales_missing']} were missing)")
    print(f"Rows after cleaning                  : {log['rows_after']}")
    print("\nMissing values after cleaning:")
    print(clean_df.isnull().sum())


# ---------------------------------------------------------------------------
# Step 4: Calculate the metrics
# ---------------------------------------------------------------------------
def calculate_metrics(df):
    """Calculate all the sales numbers we need and return them in a dictionary."""
    metrics = {}

    # Total revenue = sum of all Total_Sales values.
    metrics["total_revenue"] = float(df["Total_Sales"].sum())

    # Total units sold = sum of all Quantity values.
    metrics["total_units"] = int(df["Quantity"].sum())

    # Average sales = average value of one sale (one row).
    metrics["average_sales"] = float(df["Total_Sales"].mean())

    # Highest and lowest sale: idxmax()/idxmin() give the row position.
    highest = df.loc[df["Total_Sales"].idxmax()]
    lowest = df.loc[df["Total_Sales"].idxmin()]
    metrics["highest_sale"] = {
        "amount": float(highest["Total_Sales"]),
        "product": highest["Product"],
        "quantity": int(highest["Quantity"]),
        "date": highest["Date"].strftime("%Y-%m-%d"),
    }
    metrics["lowest_sale"] = {
        "amount": float(lowest["Total_Sales"]),
        "product": lowest["Product"],
        "quantity": int(lowest["Quantity"]),
        "date": lowest["Date"].strftime("%Y-%m-%d"),
    }

    # Product-wise performance: group rows by product and summarise each group.
    summary = df.groupby("Product").agg(
        Units_Sold=("Quantity", "sum"),
        Revenue=("Total_Sales", "sum"),
        Average_Sale=("Total_Sales", "mean"),
        Transactions=("Total_Sales", "count"),
    )
    summary["Revenue_Share_%"] = (summary["Revenue"] / metrics["total_revenue"] * 100).round(2)
    summary = summary.sort_values("Revenue", ascending=False)
    metrics["product_summary"] = summary

    # Best-selling product = the product with the most units sold.
    metrics["best_selling_product"] = summary["Units_Sold"].idxmax()
    metrics["best_selling_units"] = int(summary["Units_Sold"].max())

    # Extra: which month earned the most revenue?
    monthly = df.groupby(df["Date"].dt.to_period("M"))["Total_Sales"].sum()
    metrics["best_month"] = monthly.idxmax().strftime("%B %Y")
    metrics["best_month_revenue"] = float(monthly.max())

    # Date range and product list (used in the report).
    metrics["date_start"] = df["Date"].min().strftime("%Y-%m-%d")
    metrics["date_end"] = df["Date"].max().strftime("%Y-%m-%d")
    metrics["products"] = sorted(df["Product"].unique())

    return metrics


def print_metrics(metrics):
    """Print the calculated metrics in the console."""
    print_section("STEP 4: SALES METRICS")
    print(f"Total revenue       : {money(metrics['total_revenue'])}")
    print(f"Total units sold    : {metrics['total_units']}")
    print(f"Average sale        : {money(metrics['average_sales'])}")

    high, low = metrics["highest_sale"], metrics["lowest_sale"]
    print(f"Highest sale        : {money(high['amount'])} "
          f"({high['quantity']} x {high['product']} on {high['date']})")
    print(f"Lowest sale         : {money(low['amount'])} "
          f"({low['quantity']} x {low['product']} on {low['date']})")
    print(f"Best-selling product: {metrics['best_selling_product']} "
          f"({metrics['best_selling_units']} units)")

    print_section("STEP 5: PRODUCT-WISE SALES")
    print(metrics["product_summary"].round(2))


# ---------------------------------------------------------------------------
# Step 6: Generate the Markdown report
# ---------------------------------------------------------------------------
def generate_insights(metrics):
    """Create key insights from the real results (nothing is hard-coded)."""
    summary = metrics["product_summary"]
    insights = []

    # Product with the highest revenue.
    top_revenue = summary.index[0]
    insights.append(
        f"**{top_revenue}** earned the most revenue ({money(summary.loc[top_revenue, 'Revenue'])}), "
        f"which is {summary.loc[top_revenue, 'Revenue_Share_%']:.2f}% of all revenue."
    )

    # Best seller by units vs best seller by revenue.
    best_units = metrics["best_selling_product"]
    if best_units == top_revenue:
        insights.append(
            f"**{best_units}** is both the best-selling product by units "
            f"({metrics['best_selling_units']}) and the top product by revenue."
        )
    else:
        revenue_rank = list(summary.index).index(best_units) + 1
        insights.append(
            f"**{best_units}** sold the most units ({metrics['best_selling_units']}) "
            f"but ranks number {revenue_rank} by revenue. Units sold and revenue can rank "
            f"products differently because each product has a different price."
        )

    # Top two products' share of revenue.
    top_two_share = summary["Revenue_Share_%"].iloc[:2].sum()
    insights.append(
        f"The top two products by revenue ({summary.index[0]} and {summary.index[1]}) "
        f"together make up {top_two_share:.2f}% of total revenue."
    )

    # Lowest revenue product.
    bottom = summary.index[-1]
    insights.append(
        f"**{bottom}** brought in the least revenue ({money(summary.loc[bottom, 'Revenue'])})."
    )

    # Highest sale.
    high = metrics["highest_sale"]
    insights.append(
        f"The single biggest sale was {money(high['amount'])} "
        f"({high['quantity']} x {high['product']} on {high['date']}), "
        f"which is {high['amount'] / metrics['average_sales']:.1f} times the average sale."
    )

    # Best month.
    insights.append(
        f"{metrics['best_month']} was the strongest month with "
        f"{money(metrics['best_month_revenue'])} in revenue."
    )
    return insights


def generate_report(log, metrics, report_path=REPORT_FILE):
    """Write analysis_report.md using the real calculated results."""
    summary = metrics["product_summary"]
    insights = generate_insights(metrics)

    # Describe the missing values that were found before cleaning.
    found = [f"{col}: {n}" for col, n in log["missing_before"].items() if n > 0]
    missing_text = ", ".join(found) if found else "none"

    high, low = metrics["highest_sale"], metrics["lowest_sale"]
    lines = []

    # --- 1. Project overview ---
    lines += [
        "# Sales Data Analysis Report",
        "",
        "## 1. Project Overview",
        "",
        "This report was created automatically by `sales_analysis.py`. "
        "The project analyses sales data with Python and Pandas to find total revenue, "
        "units sold, average sales, the highest and lowest sales, the best-selling product "
        "and the performance of each product.",
        "",
    ]

    # --- 2. Dataset description ---
    lines += [
        "## 2. Dataset Description",
        "",
        f"- **File:** `sales_data.csv`",
        f"- **Rows loaded:** {log['raw_rows']}",
        f"- **Columns:** {log['raw_columns']}",
        f"- **Sales period (after cleaning):** {metrics['date_start']} to {metrics['date_end']}",
        f"- **Products:** {', '.join(metrics['products'])}",
        "",
        "| Column | Description |",
        "|---|---|",
        "| Date | Date of the sale |",
        "| Product | Name of the product sold |",
        "| Quantity | Number of units sold |",
        f"| Unit_Price | Price of one unit ({CURRENCY}) |",
        f"| Total_Sales | Quantity x Unit_Price ({CURRENCY}) |",
        "",
    ]

    # --- 3. Data cleaning steps ---
    lines += [
        "## 3. Data Cleaning Steps",
        "",
        "| Step | Result |",
        "|---|---|",
        f"| Rows loaded from CSV | {log['raw_rows']} |",
        f"| Missing values found before cleaning | {missing_text} |",
        f"| Duplicate rows removed | {log['duplicates_removed']} |",
        f"| Rows dropped because Date or Product was missing | {log['rows_dropped_missing_date_or_product']} |",
        f"| Missing Unit_Price filled with the product's median price | {log['unit_price_filled']} |",
        f"| Missing Quantity filled with the product's median quantity | {log['quantity_filled']} |",
        f"| Total_Sales recalculated as Quantity x Unit_Price | all {log['rows_after']} rows "
        f"({log['total_sales_missing']} were missing) |",
        f"| Rows left after cleaning | {log['rows_after']} |",
        "",
    ]

    # --- 4. Key metrics ---
    lines += [
        "## 4. Key Metrics",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Total Revenue | {money(metrics['total_revenue'])} |",
        f"| Total Units Sold | {metrics['total_units']} |",
        f"| Average Sale | {money(metrics['average_sales'])} |",
        f"| Highest Sale | {money(high['amount'])} ({high['quantity']} x {high['product']}, {high['date']}) |",
        f"| Lowest Sale | {money(low['amount'])} ({low['quantity']} x {low['product']}, {low['date']}) |",
        f"| Best-Selling Product (by quantity) | {metrics['best_selling_product']} "
        f"({metrics['best_selling_units']} units) |",
        "",
    ]

    # --- 5. Product-wise performance ---
    lines += [
        "## 5. Product-wise Performance",
        "",
        f"Products are sorted by revenue (highest first). Money is in {CURRENCY}.",
        "",
        "| Rank | Product | Units Sold | Revenue | Average Sale | Transactions | Revenue Share |",
        "|---|---|---|---|---|---|---|",
    ]
    for rank, (product, row) in enumerate(summary.iterrows(), start=1):
        lines.append(
            f"| {rank} | {product} | {int(row['Units_Sold'])} | {row['Revenue']:,.2f} | "
            f"{row['Average_Sale']:,.2f} | {int(row['Transactions'])} | {row['Revenue_Share_%']:.2f}% |"
        )
    lines.append("")

    # --- 6. Key insights ---
    lines += ["## 6. Key Insights", ""]
    lines += [f"{i}. {text}" for i, text in enumerate(insights, start=1)]
    lines.append("")

    # --- 7. Conclusion ---
    top_revenue = summary.index[0]
    lines += [
        "## 7. Conclusion",
        "",
        f"After cleaning, {log['rows_after']} sales records were analysed. "
        f"They generated {money(metrics['total_revenue'])} in revenue from "
        f"{metrics['total_units']} units sold, with an average sale of "
        f"{money(metrics['average_sales'])}. "
        f"{metrics['best_selling_product']} was the best-selling product by quantity and "
        f"{top_revenue} was the top product by revenue. "
        "These results can help a business decide which products to stock, promote or review.",
        "",
    ]

    # utf-8 makes sure the file reads correctly on every computer.
    Path(report_path).write_text("\n".join(lines), encoding="utf-8")
    return Path(report_path)


# ---------------------------------------------------------------------------
# Main program
# ---------------------------------------------------------------------------
def main():
    """Run the complete analysis from start to finish."""
    print_section("STEP 1: LOADING DATA")
    df = load_data(DATA_FILE)
    print(f"Loaded {len(df)} rows from {DATA_FILE.name}")

    explore_data(df)

    clean_df, log = clean_data(df)
    print_cleaning_summary(clean_df, log)

    metrics = calculate_metrics(clean_df)
    print_metrics(metrics)

    report_path = generate_report(log, metrics, REPORT_FILE)
    print_section("STEP 6: REPORT")
    print(f"Report saved to: {report_path.name}")


if __name__ == "__main__":
    main()
