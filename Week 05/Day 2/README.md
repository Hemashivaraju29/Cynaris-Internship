# Week 5 Day 2 – Automated EDA with AutoViz and SweetViz

## Objective

Explore the Indian Districts Census 2011 dataset using AutoViz and SweetViz, identify useful data insights, compare both tools, and recommend a suitable tool for business stakeholders.

## Dataset

- Dataset: Indian Districts Census 2011
- Rows: 640
- Original columns: 118

## 1. AutoViz Analysis

AutoViz was used to automatically generate visualizations for numerical variables.

Generated reports:

- Pair-wise scatter plots
- Distribution plots
- Violin plots
- Heatmap

### AutoViz Insights

1. **SC and Male_SC:** The scatter plot shows a strong positive relationship between SC population and SC male population. Districts with higher SC population generally have higher SC male population.

2. **SC and Female_SC:** The scatter plot shows a strong positive relationship between SC population and SC female population. Districts with higher SC population generally have higher SC female population.

3. **Male_SC and Female_SC:** The scatter plot shows a strong positive relationship between SC male and SC female populations across districts.

### AutoViz Report Location

`Week 05/Day 2/AutoViz_Report/AutoViz/`

## 2. SweetViz Analysis

SweetViz was used to generate a structured exploratory data analysis report.

The report contains:

- Dataset overview
- Feature information
- Missing-value information
- Distributions
- Distinct values
- Associations between variables

### SweetViz Dataset Overview

- Rows: 640
- Features: 118
- Numerical variables: 116
- Categorical variables: 1
- Text variables: 1
- State Name: 35 distinct values
- District Name: 634 distinct values

### SweetViz Report Location

`Week 05/Day 2/sweetviz_report.html`

## 3. AutoViz vs SweetViz

AutoViz is useful for quickly generating visualizations such as scatter plots, distribution plots, violin plots and heatmaps. It provides an interactive way to explore relationships between numerical variables. SweetViz provides a more structured exploratory data analysis report with detailed statistics, missing-value information, distributions, distinct values and associations in one HTML report. For this dataset, AutoViz was useful for visually identifying relationships such as the strong relationships between SC, Male_SC and Female_SC. SweetViz provided a broader overview of the dataset structure and individual feature statistics. Both tools reduce manual EDA work, but their presentation and analysis style are different.

## 4. Recommendation for Business Stakeholders

SweetViz is recommended for business stakeholders because it presents dataset statistics, missing values, distributions, distinct values and associations in a structured HTML report. This makes it easier to review the overall quality and characteristics of a dataset without manually checking every column. AutoViz is useful for technical exploratory analysis because its visualizations make relationships and distributions easy to investigate. Therefore, SweetViz can be used for communicating an overall EDA summary to stakeholders, while AutoViz can support deeper visual exploration by analysts.

## Files

- `autoviz_analysis.py`
- `sweetviz_analysis.py`
- `sweetviz_report.html`
- `AutoViz_Report/`
- `README.md`
