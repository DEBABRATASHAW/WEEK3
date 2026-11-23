"""
Tests for sales_analysis.py

Run all tests with:
    pytest -v
"""

import pandas as pd
import pytest

import sales_analysis as sa


# ---------------------------------------------------------------------------
# Fixtures: reusable data prepared once for the tests
# ---------------------------------------------------------------------------
@pytest.fixture(scope="module")
def raw_df():
    """The raw data exactly as it is in the CSV file."""
    return sa.load_data(sa.DATA_FILE)


@pytest.fixture(scope="module")
def cleaned(raw_df):
    """The cleaned data and the cleaning log."""
    return sa.clean_data(raw_df)


# ---------------------------------------------------------------------------
# 1. CSV loads successfully
# ---------------------------------------------------------------------------
def test_csv_loads_successfully(raw_df):
    assert isinstance(raw_df, pd.DataFrame)
    assert not raw_df.empty


# ---------------------------------------------------------------------------
# 2. Dataset has 100 rows
# ---------------------------------------------------------------------------
def test_dataset_has_100_rows(raw_df):
    assert len(raw_df) == 100


# ---------------------------------------------------------------------------
# 3. Required columns exist
# ---------------------------------------------------------------------------
def test_required_columns_exist(raw_df):
    for column in ["Date", "Product", "Quantity", "Unit_Price", "Total_Sales"]:
        assert column in raw_df.columns


# ---------------------------------------------------------------------------
# 4. Missing values are handled
# ---------------------------------------------------------------------------
def test_missing_values_are_handled(raw_df, cleaned):
    clean_df, _ = cleaned
    assert raw_df.isnull().sum().sum() > 0   # the raw file really has gaps
    assert clean_df.isnull().sum().sum() == 0  # and the cleaned data has none


# ---------------------------------------------------------------------------
# 5. Duplicate records are removed
# ---------------------------------------------------------------------------
def test_duplicates_are_removed(raw_df, cleaned):
    clean_df, log = cleaned
    assert raw_df.duplicated().sum() > 0     # the raw file really has duplicates
    assert clean_df.duplicated().sum() == 0  # and the cleaned data has none
    assert log["duplicates_removed"] == raw_df.duplicated().sum()


# ---------------------------------------------------------------------------
# 6. Revenue calculations are correct
# ---------------------------------------------------------------------------
def test_revenue_matches_quantity_times_price(cleaned):
    clean_df, _ = cleaned
    metrics = sa.calculate_metrics(clean_df)
    expected = (clean_df["Quantity"] * clean_df["Unit_Price"]).sum()
    assert metrics["total_revenue"] == pytest.approx(expected)
    assert metrics["total_units"] == clean_df["Quantity"].sum()


def test_calculations_on_small_example():
    """A tiny dataset where the right answers are easy to work out by hand."""
    small = pd.DataFrame({
        "Date": ["2026-01-01", "2026-01-01", "2026-01-02", "2026-01-03"],
        "Product": ["Mouse", "Mouse", "Mouse", "Mouse"],
        "Quantity": [2, 2, None, 4],          # row 3 has a missing Quantity
        "Unit_Price": [500, 500, 500, None],  # row 4 has a missing Unit_Price
        "Total_Sales": [1000, 1000, None, 2000],
    })
    clean_df, log = sa.clean_data(small)
    metrics = sa.calculate_metrics(clean_df)

    assert log["duplicates_removed"] == 1                 # rows 1 and 2 are identical
    assert len(clean_df) == 3
    # Quantities: 2, median(2, 4) = 3, 4 -> 9 units
    assert metrics["total_units"] == 9
    # Sales: 2x500 + 3x500 + 4x500 = 4500
    assert metrics["total_revenue"] == pytest.approx(4500)
    assert metrics["average_sales"] == pytest.approx(1500)
    assert metrics["highest_sale"]["amount"] == pytest.approx(2000)
    assert metrics["lowest_sale"]["amount"] == pytest.approx(1000)


# ---------------------------------------------------------------------------
# 7. Report is generated successfully
# ---------------------------------------------------------------------------
def test_report_is_generated(cleaned, tmp_path):
    clean_df, log = cleaned
    metrics = sa.calculate_metrics(clean_df)

    # tmp_path is a temporary folder, so the real report is not overwritten.
    report_file = tmp_path / "test_report.md"
    sa.generate_report(log, metrics, report_path=report_file)

    assert report_file.exists()
    text = report_file.read_text(encoding="utf-8")
    assert "# Sales Data Analysis Report" in text
    assert "Total Revenue" in text
    assert sa.money(metrics["total_revenue"]) in text  # real result is in the report
