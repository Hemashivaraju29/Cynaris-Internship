# W8D2: Business Recommendations — AI Narrative from Analytics

## Overview

This project analyzes a CSV dataset, calculates five data insights, uses
Groq AI to generate an executive summary and actionable business
recommendations, and exports the results to a PowerPoint presentation.

## Features

- CSV-based exploratory data analysis using Pandas.
- Five insights covering dataset size, average, maximum, minimum, and
  regional sales performance where applicable.
- Groq-powered executive narrative of approximately 200 words.
- Prioritized business recommendations with suggested KPIs.
- Seven-slide PowerPoint export using python-pptx.
- Automated tests for analysis, validation, and presentation generation.

## Project Structure

```text
Day 2/
├── business_recommendations.py
├── ppt_export.py
├── run_pipeline.py
├── README.md
├── .gitignore
├── tests/
│   └── test_w8d2.py
└── output/
```

## Requirements

- Python 3.11+
- pandas
- python-dotenv
- groq
- python-pptx
- pytest

Install any missing dependencies in your virtual environment:

```powershell
pip install pandas python-dotenv groq python-pptx pytest
```

## Configuration

Create or update the project-root `.env` file with your own Groq credentials:

```text
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=your_supported_groq_model
```

Never commit `.env` or share your API key.

## Run the Pipeline

From the repository root:

```powershell
python "Week 08\Day 2\run_pipeline.py" "Week 07\Day 3\Sales_Data.csv"
```

Specify a different PowerPoint output path if needed:

```powershell
python "Week 08\Day 2\run_pipeline.py" "Week 07\Day 3\Sales_Data.csv" --output "Week 08\Day 2\output\business_recommendations.pptx"
```

## Run Tests

```powershell
python -m pytest "Week 08\Day 2\tests\test_w8d2.py" -v
```

The automated tests validate insight calculation, invalid datasets,
narrative input validation, and seven-slide PowerPoint generation.
They do not require a live Groq API call.

## Output

The generated presentation contains:

1. Title slide.
2. Five individual data-insight slides.
3. Executive summary and business recommendations slide.

AI recommendations should be reviewed by business stakeholders before
being used for decisions. Recommendations depend on the quality and
coverage of the supplied data.
