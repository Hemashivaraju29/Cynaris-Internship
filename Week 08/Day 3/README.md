# W8D3: PPT Report Export Using python-pptx

## Overview

This project automates the generation of an executive PowerPoint report from CSV data using Pandas, Groq, and python-pptx.

## Features

- Load and validate CSV data.
- Calculate five key data insights.
- Generate an executive summary and business recommendations using the Groq API.
- Export a seven-slide PowerPoint presentation.
- Validate core functionality using automated pytest tests.

## Project Structure

- `business_recommendations.py` — calculates insights and generates the AI narrative.
- `ppt_export.py` — builds and saves the PowerPoint presentation.
- `run_pipeline.py` — runs the end-to-end workflow.
- `tests/test_w8d3.py` — automated tests.
- `output/` — generated PowerPoint reports; output files are excluded from Git.

## Requirements

- Python 3.11+
- pandas
- python-dotenv
- groq
- python-pptx
- pytest

## Environment Setup

Configure `GROQ_API_KEY` in the repository's local `.env` file. Never commit the API key.

## Run the Pipeline

```powershell
python "Week 08\Day 3\run_pipeline.py" "Week 07\Day 3\Sales_Data.csv"
```

## Run Tests

```powershell
python -m pytest "Week 08\Day 3\tests\test_w8d3.py" -v
```

## Presentation Structure

1. Title slide
2. Data Insight 1
3. Data Insight 2
4. Data Insight 3
5. Data Insight 4
6. Data Insight 5
7. Executive Summary and Business Recommendations

## Validation

The pipeline was executed successfully using the sample sales dataset. The generated PowerPoint contained seven slides, and all seven automated tests passed.

## Business Value

Automated reporting reduces repetitive manual work and helps stakeholders review key findings and potential business actions more efficiently.
