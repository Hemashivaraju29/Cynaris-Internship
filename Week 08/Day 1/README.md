\# Week 8 Day 1 — Executive Summary Generation via Groq



\## Overview



This project analyzes a sales CSV dataset, generates five data insights using Pandas, creates an executive summary using the Groq API, and exports the results to a PowerPoint presentation.



\## Features



\- Reads sales data from a CSV file.

\- Calculates five data insights, including average, highest, and lowest sales and the region with the highest total sales.

\- Generates a business-focused executive summary using Groq.

\- Exports a seven-slide PowerPoint presentation using `python-pptx`.

\- Includes automated tests for insight calculation, validation, and PowerPoint generation.



\## Requirements



\- Python 3.11+

\- pandas

\- groq

\- python-dotenv

\- python-pptx

\- pytest



\## Setup



1\. Activate your Python virtual environment.

2\. Install dependencies if required:



&#x20;  ```powershell

&#x20;  python -m pip install pandas groq python-dotenv python-pptx pytest

&#x20;  ```



3\. Configure your Groq API key in the root `.env` file:



&#x20;  ```dotenv

&#x20;  GROQ\_API\_KEY=your\_groq\_api\_key

&#x20;  GROQ\_MODEL=openai/gpt-oss-120b

&#x20;  ```



&#x20;  Replace the placeholder with your own API key. Never commit the `.env` file.



\## Run the Pipeline



From the repository root:



```powershell

python "Week 08\\Day 1\\run\_pipeline.py" "Week 07\\Day 3\\Sales\_Data.csv"

```



The generated presentation is saved to:



`Week 08\\Day 1\\output\\executive\_summary.pptx`



\## Run Automated Tests



```powershell

python -m pytest "Week 08\\Day 1\\tests\\test\_w8d1.py" -v

```



The tests validate five-insight generation, empty-data handling, seven-slide PowerPoint creation, and invalid insight-count handling.



\## PowerPoint Structure



1\. Executive Data Summary — title slide

2\. Insight 1

3\. Insight 2

4\. Insight 3

5\. Insight 4

6\. Insight 5

7\. Executive Summary \& Recommendations



\## Technologies



Python, Pandas, Groq API, python-dotenv, python-pptx, and pytest.



