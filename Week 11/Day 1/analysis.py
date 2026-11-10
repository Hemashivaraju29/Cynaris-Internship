
from pathlib import Path
import json

import pandas as pd
import plotly.express as px


# Project paths
PROJECT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PROJECT_DIR.parents[1]

DATA_PATH = PROJECT_ROOT / "Week 07" / "Day 3" / "Sales_Data.csv"
OUTPUT_DIR = PROJECT_DIR / "outputs"


def load_data(file_path=DATA_PATH):
    """Load and validate the sales dataset."""
    required_columns = {
        "Date", "Region", "Category", "Sales", "Units Sold"
    }

    df = pd.read_csv(file_path)

    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
    df["Units Sold"] = pd.to_numeric(
        df["Units Sold"], errors="coerce"
    )

    df = df.dropna(
        subset=["Date", "Region", "Category", "Sales", "Units Sold"]
    )

    if df.empty:
        raise ValueError("No valid sales records found.")

    if (df["Sales"] < 0).any() or (df["Units Sold"] < 0).any():
        raise ValueError("Sales and units sold cannot be negative.")

    return df.sort_values("Date").reset_index(drop=True)


def analyze_sales(df):
    """Calculate business performance metrics."""
    region_sales = (
        df.groupby("Region")
        .agg(
            Total_Sales=("Sales", "sum"),
            Units_Sold=("Units Sold", "sum"),
            Transactions=("Sales", "count"),
        )
        .sort_values("Total_Sales", ascending=False)
    )

    category_sales = (
        df.groupby("Category")
        .agg(
            Total_Sales=("Sales", "sum"),
            Units_Sold=("Units Sold", "sum"),
            Transactions=("Sales", "count"),
        )
        .sort_values("Total_Sales", ascending=False)
    )

    monthly_sales = (
        df.set_index("Date")["Sales"]
        .resample("MS")
        .sum()
        .rename("Total_Sales")
        .reset_index()
    )

    total_sales = float(df["Sales"].sum())
    total_units = int(df["Units Sold"].sum())

    insights = {
        "total_sales": total_sales,
        "total_units": total_units,
        "total_transactions": len(df),
        "average_transaction_value": float(df["Sales"].mean()),
        "top_region": str(region_sales.index[0]),
        "top_region_sales": float(region_sales.iloc[0]["Total_Sales"]),
        "lowest_region": str(region_sales.index[-1]),
        "top_category": str(category_sales.index[0]),
        "top_category_sales": float(
            category_sales.iloc[0]["Total_Sales"]
        ),
        "highest_month": monthly_sales.loc[
            monthly_sales["Total_Sales"].idxmax(), "Date"
        ].strftime("%B %Y"),
        "highest_month_sales": float(monthly_sales["Total_Sales"].max()),
        "lowest_month": monthly_sales.loc[
            monthly_sales["Total_Sales"].idxmin(), "Date"
        ].strftime("%B %Y"),
        "lowest_month_sales": float(monthly_sales["Total_Sales"].min()),
    }

    return region_sales, category_sales, monthly_sales, insights


def create_visualizations(
    region_sales, category_sales, monthly_sales, output_dir=OUTPUT_DIR
):
    """Create interactive charts and save them as HTML."""
    output_dir.mkdir(parents=True, exist_ok=True)

    charts = {
        "regional_sales.html": px.bar(
            region_sales.reset_index(),
            x="Region",
            y="Total_Sales",
            title="Regional Sales Performance",
            text_auto=True,
        ),
        "category_sales.html": px.bar(
            category_sales.reset_index(),
            x="Category",
            y="Total_Sales",
            title="Category-wise Sales Performance",
            text_auto=True,
        ),
        "monthly_sales.html": px.line(
            monthly_sales,
            x="Date",
            y="Total_Sales",
            title="Monthly Sales Trend",
            markers=True,
        ),
        "units_by_category.html": px.bar(
            category_sales.reset_index(),
            x="Category",
            y="Units_Sold",
            title="Units Sold by Category",
            text_auto=True,
        ),
    }

    for filename, figure in charts.items():
        y_label = (
            "Units Sold"
            if filename == "units_by_category.html"
            else "Sales (INR)"
        )

        figure.update_layout(
            template="plotly_white",
            yaxis_title=y_label,
            font=dict(size=13),
        )

        figure.write_html(str(output_dir / filename))

    return list(charts.keys())


def save_report(insights, region_sales, category_sales, monthly_sales):
    """Save the findings as a structured JSON report."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    report = {
        "business_summary": insights,
        "regional_performance": region_sales.reset_index().to_dict(
            orient="records"
        ),
        "category_performance": category_sales.reset_index().to_dict(
            orient="records"
        ),
        "monthly_performance": monthly_sales.assign(
            Date=monthly_sales["Date"].dt.strftime("%Y-%m-%d")
        ).to_dict(orient="records"),
    }

    report_path = OUTPUT_DIR / "storytelling_report.json"

    with report_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    return report_path


def main():
    print("DATA STORYTELLING ANALYSIS")
    print("=" * 45)

    df = load_data()

    region, category, monthly, insights = analyze_sales(df)

    print(f"\nRecords analysed: {len(df)}")
    print(f"Total sales: Rs. {insights['total_sales']:,.2f}")
    print(f"Total units sold: {insights['total_units']}")
    print(f"Average transaction value: Rs. "
          f"{insights['average_transaction_value']:,.2f}")

    print("\nREGIONAL PERFORMANCE")
    print(region)

    print("\nCATEGORY PERFORMANCE")
    print(category)

    print("\nMONTHLY SALES")
    print(monthly.to_string(index=False))

    print("\nKEY BUSINESS INSIGHTS")
    print(f"Highest-performing region: {insights['top_region']}")
    print(f"Lowest-performing region: {insights['lowest_region']}")
    print(f"Top category: {insights['top_category']}")
    print(f"Best sales month: {insights['highest_month']}")
    print(f"Lowest sales month: {insights['lowest_month']}")

    charts = create_visualizations(region, category, monthly)
    report_path = save_report(insights, region, category, monthly)

    print("\nOUTPUTS CREATED")
    for chart in charts:
        print(f"- outputs/{chart}")

    print(f"- {report_path}")
    print("\nAnalysis completed successfully.")


if __name__ == "__main__":
    main()
