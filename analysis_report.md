# Sales Data Analysis Report

## 1. Project Overview

This report was created automatically by `sales_analysis.py`. The project analyses sales data with Python and Pandas to find total revenue, units sold, average sales, the highest and lowest sales, the best-selling product and the performance of each product.

## 2. Dataset Description

- **File:** `sales_data.csv`
- **Rows loaded:** 100
- **Columns:** 7
- **Sales period (after cleaning):** 2024-01-01 to 2024-04-09
- **Products:** Headphones, Laptop, Monitor, Phone, Tablet

| Column | Description |
|---|---|
| Date | Date of the sale |
| Product | Name of the product sold |
| Quantity | Number of units sold |
| Unit_Price | Price of one unit (INR) |
| Total_Sales | Quantity x Unit_Price (INR) |

## 3. Data Cleaning Steps

| Step | Result |
|---|---|
| Rows loaded from CSV | 100 |
| Missing values found before cleaning | none |
| Duplicate rows removed | 0 |
| Rows dropped because Date or Product was missing | 0 |
| Missing Unit_Price filled with the product's median price | 0 |
| Missing Quantity filled with the product's median quantity | 0 |
| Total_Sales recalculated as Quantity x Unit_Price | all 100 rows (0 were missing) |
| Rows left after cleaning | 100 |

## 4. Key Metrics

| Metric | Value |
|---|---|
| Total Revenue | INR 12,365,048.00 |
| Total Units Sold | 478 |
| Average Sale | INR 123,650.48 |
| Highest Sale | INR 373,932.00 (9 x Phone, 2024-01-16) |
| Lowest Sale | INR 6,540.00 (5 x Tablet, 2024-02-23) |
| Best-Selling Product (by quantity) | Laptop (136 units) |

## 5. Product-wise Performance

Products are sorted by revenue (highest first). Money is in INR.

| Rank | Product | Units Sold | Revenue | Average Sale | Transactions | Revenue Share |
|---|---|---|---|---|---|---|
| 1 | Laptop | 136 | 3,889,210.00 | 162,050.42 | 24 | 31.45% |
| 2 | Tablet | 127 | 2,884,340.00 | 110,936.15 | 26 | 23.33% |
| 3 | Phone | 101 | 2,859,394.00 | 142,969.70 | 20 | 23.12% |
| 4 | Headphones | 48 | 1,384,033.00 | 92,268.87 | 15 | 11.19% |
| 5 | Monitor | 66 | 1,348,071.00 | 89,871.40 | 15 | 10.90% |

## 6. Key Insights

1. **Laptop** earned the most revenue (INR 3,889,210.00), which is 31.45% of all revenue.
2. **Laptop** is both the best-selling product by units (136) and the top product by revenue.
3. The top two products by revenue (Laptop and Tablet) together make up 54.78% of total revenue.
4. **Monitor** brought in the least revenue (INR 1,348,071.00).
5. The single biggest sale was INR 373,932.00 (9 x Phone on 2024-01-16), which is 3.0 times the average sale.
6. March 2024 was the strongest month with INR 4,485,006.00 in revenue.

## 7. Conclusion

After cleaning, 100 sales records were analysed. They generated INR 12,365,048.00 in revenue from 478 units sold, with an average sale of INR 123,650.48. Laptop was the best-selling product by quantity and Laptop was the top product by revenue. These results can help a business decide which products to stock, promote or review.
