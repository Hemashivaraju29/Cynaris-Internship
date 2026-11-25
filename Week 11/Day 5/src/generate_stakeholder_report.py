from pathlib import Path
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs"
REPORT_PATH = OUTPUT_DIR / "W11D5_Stakeholder_Business_Insights_Report.docx"

# Load generated analysis results
df = pd.read_csv(BASE_DIR.parents[1] / "Week 07" / "Day 3" / "Sales_Data.csv")
region = pd.read_csv(OUTPUT_DIR / "regional_sales.csv", index_col=0)
category = pd.read_csv(OUTPUT_DIR / "category_sales.csv", index_col=0)
monthly = pd.read_csv(OUTPUT_DIR / "monthly_sales.csv", index_col=0)
performance = pd.read_csv(OUTPUT_DIR / "category_performance.csv", index_col=0)

total_sales = df["Sales"].sum()
total_units = df["Units Sold"].sum()
avg_transaction = df["Sales"].mean()
transaction_count = len(df)

top_region = region["Total Sales"].idxmax()
top_region_sales = region.loc[top_region, "Total Sales"]
top_category = category["Total Sales"].idxmax()
top_category_sales = category.loc[top_category, "Total Sales"]
top_month = monthly["Total Sales"].idxmax()
top_month_sales = monthly.loc[top_month, "Total Sales"]
top_units_category = performance["Units"].idxmax()
top_units = performance.loc[top_units_category, "Units"]
top_revenue_per_unit = performance["Revenue Per Unit"].idxmax()
top_rpu = performance.loc[top_revenue_per_unit, "Revenue Per Unit"]

doc = Document()

# Document styling
styles = doc.styles
styles["Normal"].font.name = "Calibri"
styles["Normal"].font.size = Pt(10)
styles["Title"].font.color.rgb = RGBColor(31, 78, 121)
styles["Heading 1"].font.color.rgb = RGBColor(31, 78, 121)
styles["Heading 2"].font.color.rgb = RGBColor(46, 116, 181)

# Cover heading
title = doc.add_heading("STAKEHOLDER BUSINESS INSIGHTS REPORT", 0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

subtitle = doc.add_paragraph("Week 11 | Day 5 | Cynaris Sales Analysis")
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_paragraph("Reporting period: January to September 2026")
doc.add_paragraph("Prepared for: Business Stakeholders")
doc.add_paragraph("Dataset: Cynaris Sales Data (24 transactions)")

doc.add_heading("1. Executive Summary", level=1)
doc.add_paragraph(
    f"The analysis covers {transaction_count} sales transactions across four "
    f"regions and four product categories from January to September 2026. "
    f"Total revenue was Rs. {total_sales:,.0f}, with {total_units:,} units sold "
    f"and an average transaction value of Rs. {avg_transaction:,.0f}. "
    f"South was the leading region, Electronics generated the highest category "
    f"revenue, and June recorded the highest monthly sales."
)

doc.add_heading("2. Overall Business Performance", level=1)
table = doc.add_table(rows=1, cols=2)
table.style = "Light Shading Accent 1"
table.rows[0].cells[0].text = "Metric"
table.rows[0].cells[1].text = "Result"

metrics = [
    ("Total Revenue", f"Rs. {total_sales:,.0f}"),
    ("Total Units Sold", f"{total_units:,}"),
    ("Number of Transactions", str(transaction_count)),
    ("Average Transaction Value", f"Rs. {avg_transaction:,.0f}"),
]
for metric, value in metrics:
    cells = table.add_row().cells
    cells[0].text = metric
    cells[1].text = value

doc.add_heading("3. Five Key Business Insights", level=1)

insights = [
    (
        "Insight 1: South is the highest-revenue region",
        f"South generated Rs. {top_region_sales:,.0f}, the highest among all "
        f"regions, contributing {top_region_sales / total_sales * 100:.1f}% "
        "of total revenue.",
        "South is an important contributor to overall sales performance. "
        "Its sales practices and customer demand can be studied for useful patterns.",
        "Review successful sales activities in South and identify opportunities "
        "to apply suitable practices in other regions."
    ),
    (
        "Insight 2: Electronics is the leading revenue category",
        f"Electronics generated Rs. {top_category_sales:,.0f}, contributing "
        f"{top_category_sales / total_sales * 100:.1f}% of total revenue.",
        "Electronics is the largest revenue contributor in the current dataset. "
        "Changes in its demand may significantly affect overall sales.",
        "Monitor Electronics demand, maintain suitable inventory, and evaluate "
        "promotional opportunities."
    ),
    (
        "Insight 3: June recorded the highest monthly sales",
        f"{top_month} recorded the highest sales of Rs. {top_month_sales:,.0f}.",
        "Monthly sales vary during the reporting period. Understanding the "
        "factors behind June's performance may help improve planning.",
        "Review June's product mix, regional contribution, and sales activities "
        "before planning future campaigns."
    ),
    (
        "Insight 4: Grocery leads in units sold, not revenue",
        f"Grocery sold {top_units:,} units, representing "
        f"{top_units / total_units * 100:.1f}% of units sold, but generated "
        f"only Rs. {category.loc['Grocery', 'Total Sales']:,.0f} "
        f"({category.loc['Grocery', 'Total Sales'] / total_sales * 100:.1f}% "
        "of revenue).",
        "Grocery has high sales volume but a comparatively low revenue "
        "contribution. Unit volume alone does not explain revenue performance.",
        "Review product pricing, product mix, and opportunities for relevant "
        "bundles while monitoring customer demand."
    ),
    (
        "Insight 5: Furniture has the highest revenue per unit",
        f"Furniture generated Rs. {top_rpu:,.2f} per unit, the highest "
        "among the four categories.",
        "Furniture contributes a higher average revenue for each unit sold. "
        "However, revenue per unit is not the same as profit per unit.",
        "Evaluate Furniture demand and sales opportunities. Compare product "
        "costs and margins before making profitability decisions."
    ),
]

for heading, evidence, impact, recommendation in insights:
    doc.add_heading(heading, level=2)
    doc.add_paragraph("Evidence: " + evidence)
    doc.add_paragraph("Business impact: " + impact)
    doc.add_paragraph("Recommendation: " + recommendation)

doc.add_heading("4. Supporting Visualizations", level=1)

charts = [
    ("Sales by Region", "sales_by_region.png"),
    ("Sales by Category", "sales_by_category.png"),
    ("Monthly Sales Trend", "monthly_sales_trend.png"),
    ("Units Sold by Category", "units_by_category.png"),
]

for heading, filename in charts:
    doc.add_heading(heading, level=2)
    chart_path = OUTPUT_DIR / filename
    if chart_path.exists():
        doc.add_picture(str(chart_path), width=Inches(5.8))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_heading("5. Management Recommendations", level=1)
recommendations = [
    "Study South's sales performance to identify practices that may work in other regions.",
    "Monitor Electronics demand and maintain suitable inventory levels.",
    "Investigate the factors behind June's sales performance.",
    "Review Grocery pricing and product mix while maintaining its strong unit volume.",
    "Assess product costs and margins before drawing conclusions about category profitability.",
]
for item in recommendations:
    doc.add_paragraph(item, style="List Bullet")

doc.add_heading("6. Conclusion", level=1)
doc.add_paragraph(
    "The analysis highlights important differences in regional sales, category "
    "revenue, monthly performance, unit volume, and revenue per unit. These "
    "findings provide stakeholders with a clear starting point for improving "
    "sales planning and monitoring business performance. Recommendations "
    "should be validated with additional periods of data, costs, margins, "
    "and customer information before major business decisions are made."
)

doc.add_heading("7. Scope and Limitations", level=1)
doc.add_paragraph(
    "This report is based on 24 transactions covering January to September 2026. "
    "It describes the available dataset and does not establish the causes of "
    "sales differences. Profitability, customer behaviour, marketing impact, "
    "and year-over-year growth cannot be determined without additional data."
)

# Footer
for section in doc.sections:
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer.add_run("Cynaris Solutions | W11D5 Stakeholder Report")

doc.save(REPORT_PATH)
print(f"Stakeholder report created: {REPORT_PATH}")
print(f"Insights included: {len(insights)}")
print(f"Charts included: {sum((OUTPUT_DIR / name).exists() for _, name in charts)}")
