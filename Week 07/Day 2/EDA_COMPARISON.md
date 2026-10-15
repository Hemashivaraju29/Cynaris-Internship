# Week 7 Day 2: AutoViz and SweetViz Comparison

## 1. Dataset Overview

- Dataset: Nifty 500 stock-price sample
- Records: 7,395
- Columns: 8
- Date range: 2012-01-02 to 2021-12-31
- Companies represented: Reliance, TCS, and HDFC Bank
- Missing values: 0

## 2. Three Key Insights

### Insight 1: Equal Company Coverage
Reliance, TCS, and HDFC Bank each have 2,465 records. The dataset contains no missing values, making it suitable for this exploratory analysis.

### Insight 2: Closing-Price Differences
TCS has the highest average closing price at 1,589.00, followed by Reliance at 926.73 and HDFC Bank at 774.37. These figures describe share prices, not overall company value or investment performance.

### Insight 3: Highest Combined Daily Trading Volume
The highest combined daily trading volume across the three companies was 210,705,356 on 17 February 2017.

## 3. AutoViz vs SweetViz: 100-Word Comparison

AutoViz and SweetViz both turn the same dataset into visual summaries, but they support different workflows. AutoViz generates multiple chart-focused HTML files, including numeric distributions, categorical plots, heatmaps, pairwise scatter plots, time-series plots, and violin plots. This helps analysts explore distributions, relationships, and trends across visualizations. SweetViz creates one consolidated HTML report with feature-level summaries, making it convenient for a quick overview in one place. For this dataset, AutoViz is useful for deeper chart-based exploration, while SweetViz is easier to review at a glance. Both tools support exploratory analysis, but neither establishes causation. Analysts should validate findings with calculations reliably.

## 4. Recommendation for Business Stakeholders

I recommend SweetViz for business stakeholders who need a quick, accessible overview of the dataset. Its single HTML report is easier to open, navigate, and share than multiple separate chart files. AutoViz is a useful companion for analysts who need to investigate detailed distributions, relationships, and time-series patterns. For reliable decisions, stakeholders should review the report alongside verified summary statistics and business context.

## 5. Deliverables

- `run_autoviz.py` — generates AutoViz visualizations.
- `autoviz_plots/` — contains six HTML visualization files.
- `run_sweetviz.py` — generates the SweetViz report.
- `sweetviz_report.html` — consolidated SweetViz report.
- `calculate_insights.py` — calculates dataset summary statistics.
- `EDA_COMPARISON.md` — findings, comparison, and recommendation.

