from pathlib import Path

import pandas as pd
import plotly.express as px
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt


ROOT = Path(__file__).resolve().parents[3]
DATA_FILE = ROOT / "Week 07" / "Day 3" / "Sales_Data.csv"
OUTPUT_DIR = ROOT / "Week 11" / "Day 2" / "outputs"
CHART_DIR = OUTPUT_DIR / "charts"


def load_data():
    """Load and validate the sales dataset."""
    df = pd.read_csv(DATA_FILE)

    required = {"Date", "Region", "Category", "Sales", "Units Sold"}
    missing = required - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
    df["Units Sold"] = pd.to_numeric(df["Units Sold"], errors="coerce")

    if df[list(required)].isnull().any().any():
        raise ValueError("Dataset contains missing or invalid required values.")

    if (df["Sales"] < 0).any() or (df["Units Sold"] < 0).any():
        raise ValueError("Sales and units sold cannot be negative.")

    return df


def analyse_data(df):
    """Calculate executive-level sales metrics."""
    regional = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
    category = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
    monthly = (
        df.assign(Month=df["Date"].dt.to_period("M").astype(str))
        .groupby("Month")["Sales"]
        .sum()
        .sort_index()
    )

    return {
        "total_sales": df["Sales"].sum(),
        "average_sales": df["Sales"].mean(),
        "total_units": df["Units Sold"].sum(),
        "transactions": len(df),
        "regional": regional,
        "category": category,
        "monthly": monthly,
    }


def create_plotly_charts(metrics):
    """Create interactive HTML charts using Plotly."""
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    charts = {
        "regional_sales.html": px.bar(
            x=metrics["regional"].index,
            y=metrics["regional"].values,
            title="Sales Performance by Region",
            labels={"x": "Region", "y": "Sales (INR)"},
        ),
        "category_sales.html": px.bar(
            x=metrics["category"].index,
            y=metrics["category"].values,
            title="Sales Performance by Category",
            labels={"x": "Category", "y": "Sales (INR)"},
        ),
        "monthly_sales.html": px.line(
            x=metrics["monthly"].index,
            y=metrics["monthly"].values,
            markers=True,
            title="Monthly Sales Trend",
            labels={"x": "Month", "y": "Sales (INR)"},
        ),
    }

    for filename, figure in charts.items():
        figure.update_layout(template="plotly_white")
        figure.write_html(str(CHART_DIR / filename))


def add_text(slide, text, left, top, width, height, size=20, bold=False):
    """Add formatted text to a PowerPoint slide."""
    box = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    paragraph = box.text_frame.paragraphs[0]
    paragraph.text = text
    paragraph.font.size = Pt(size)
    paragraph.font.bold = bold
    return box


def add_bar_chart(slide, title, series, left=0.8, top=1.5):
    """Add an editable PowerPoint column chart."""
    chart_data = CategoryChartData()
    chart_data.categories = [str(x) for x in series.index]
    chart_data.add_series("Sales (INR)", [float(x) for x in series.values])

    slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED,
        Inches(left),
        Inches(top),
        Inches(8.5),
        Inches(4.8),
        chart_data,
    )


def create_powerpoint(metrics):
    """Build the executive PowerPoint report."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    # Slide 1: Title and key metrics
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_text(slide, "Executive Sales Report", 0.8, 0.8, 8.5, 0.8, 30, True)
    add_text(slide, "Business Performance Overview | 2026", 0.8, 1.8, 8, 0.5, 18)
    add_text(
        slide,
        f"Total Revenue: INR {metrics['total_sales']:,.0f}\n"
        f"Average Transaction: INR {metrics['average_sales']:,.0f}\n"
        f"Units Sold: {metrics['total_units']:,.0f}\n"
        f"Transactions: {metrics['transactions']}",
        1.0, 3.0, 7.5, 2.5, 22,
    )

    # Slide 2: Regional performance
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_text(slide, "Regional Sales Performance", 0.6, 0.4, 8.5, 0.7, 25, True)
    add_bar_chart(slide, "Regional Sales", metrics["regional"])
    add_text(
        slide,
        f"Top region: {metrics['regional'].idxmax()} "
        f"(INR {metrics['regional'].max():,.0f})",
        0.8, 6.4, 8, 0.4, 16,
    )

    # Slide 3: Category performance
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_text(slide, "Category Sales Performance", 0.6, 0.4, 8.5, 0.7, 25, True)
    add_bar_chart(slide, "Category Sales", metrics["category"])
    add_text(
        slide,
        f"Leading category: {metrics['category'].idxmax()} "
        f"(INR {metrics['category'].max():,.0f})",
        0.8, 6.4, 8, 0.4, 16,
    )

    # Slide 4: Monthly performance
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_text(slide, "Monthly Sales Trend", 0.6, 0.4, 8.5, 0.7, 25, True)
    add_bar_chart(slide, "Monthly Sales", metrics["monthly"])
    add_text(
        slide,
        f"Best month: {metrics['monthly'].idxmax()} "
        f"(INR {metrics['monthly'].max():,.0f})",
        0.8, 6.4, 8, 0.4, 16,
    )

    # Slide 5: Executive recommendations
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_text(slide, "Executive Summary & Recommendations", 0.6, 0.5, 9, 0.8, 24, True)

    recommendations = [
        f"1. Strengthen strategies in {metrics['regional'].idxmax()}, the leading region.",
        f"2. Review opportunities to grow {metrics['category'].idxmax()} sales.",
        f"3. Investigate weaker months and identify seasonal patterns.",
        "4. Monitor sales and units sold regularly to support decisions.",
        "5. Collect more customer and cost data for deeper analysis.",
    ]

    add_text(slide, "\n\n".join(recommendations), 0.9, 1.8, 8.5, 4.5, 17)

    report_path = OUTPUT_DIR / "executive_report.pptx"
    prs.save(report_path)
    return report_path


def main():
    df = load_data()
    metrics = analyse_data(df)
    create_plotly_charts(metrics)
    report = create_powerpoint(metrics)

    print(f"Transactions analysed: {metrics['transactions']}")
    print(f"Total sales: INR {metrics['total_sales']:,.2f}")
    print(f"Total units sold: {metrics['total_units']}")
    print(f"PowerPoint saved: {report}")
    print(f"Interactive charts saved: {CHART_DIR}")


if __name__ == "__main__":
    main()
