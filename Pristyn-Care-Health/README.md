# Pristyn Care Health – Healthcare Data Analytics

## 1. Project Overview

This project focuses on analysing healthcare appointment data, patient satisfaction, and hospital resource utilisation to identify operational trends and opportunities for improvement.

The objective is to use data analytics to support better appointment management, patient experience, and healthcare operations.

## 2. Project Structure

```text
Pristyn-Care-Health/
│
├── data/               # Original datasets (excluded from Git)
├── src/                # Python analysis scripts
├── sql/                # SQL analysis queries
├── outputs/            # Generated analysis reports
├── reports/            # Executive summary and A/B test proposals
├── docs/               # Project documentation
└── dashboard/          # Streamlit dashboard
```

## 3. Datasets

Three datasets were used for analysis.

| Dataset                 |   Records | Columns |
| ----------------------- | --------: | ------: |
| Healthcare Appointments |     2,000 |      15 |
| Patient Satisfaction    |       600 |      13 |
| Resource Utilisation    |       400 |      14 |
| **Total**               | **3,000** |         |

### Healthcare Appointments

Contains appointment dates, departments, specialties, waiting times, consultation duration, insurance types, and no-show information.

### Patient Satisfaction

Contains doctor, nurse, cleanliness, billing, and overall satisfaction ratings, along with waiting times and recommendation responses.

### Resource Utilisation

Contains bed occupancy, ICU capacity, scheduled and completed surgeries, staff attendance, waiting times, and readmission counts.

## 4. Data Quality Analysis

- No duplicate rows were identified in the three datasets.
- The appointments dataset contains no missing values.
- The patient satisfaction dataset contains 163 missing feedback comments.
- The resource utilisation dataset contains no missing values.
- Resource validation identified records where occupied beds exceeded total beds, ICU occupancy exceeded ICU capacity, or completed surgeries exceeded scheduled surgeries.

## 5. Appointment No-Show Analysis

A total of 2,000 appointments were analysed.

| Metric                | Result |
| --------------------- | -----: |
| Total appointments    |  2,000 |
| Attended appointments |  1,676 |
| No-show appointments  |    324 |
| Overall no-show rate  | 16.20% |

### Key Findings

- Emergency had the highest department no-show rate at 18.00%.
- General Medicine had the highest specialty no-show rate at 22.50%.
- Dermatology recorded a no-show rate of 20.46%.

## 6. Statistical Analysis

Chi-square tests were performed to examine the association between appointment no-show status and selected factors.

Specialty showed a statistically significant association with no-show status (p = 0.000031).

Department, patient age group, insurance type, and booking hour did not show statistically significant associations at the 5% level.

The findings indicate association, not causation. Multiple-testing correction and expected cell count checks should be considered when interpreting the results.

## 7. Patient Satisfaction Analysis

A total of 600 patient satisfaction surveys were analysed.

| Metric                 | Average |
| ---------------------- | ------: |
| Doctor rating          |    2.92 |
| Nurse rating           |    2.96 |
| Cleanliness rating     |    3.04 |
| Billing clarity rating |    2.93 |
| Overall satisfaction   |    3.04 |

### Hospital Comparison

- Sunrise South: 3.37
- Sunrise North: 3.09
- Sunrise Main Campus: 2.92
- Sunrise East: 2.81

The results indicate opportunities to improve billing communication and patient experience, particularly at Sunrise East.

Average patient waiting time was 91.43 minutes.

## 8. Resource Data Quality Analysis

The resource utilisation dataset contained 400 records.

A total of 337 records (84.25%) had at least one validation issue.

Identified issues included:

- Occupied beds exceeding total beds.
- ICU occupied beds exceeding ICU capacity.
- Completed surgeries exceeding scheduled surgeries.

These records require investigation before reliable resource utilisation KPIs can be reported.

## 9. SQL Database and Analysis

SQLite was used to create a database named `pristyn_healthcare.db`.

Three tables were created:

- `healthcare_appointments`
- `patient_satisfaction`
- `resource_utilisation`

SQL queries were executed to analyse:

- Overall appointment performance.
- Department-wise no-show rates.
- Specialty-wise no-show rates.
- Patient satisfaction ratings.
- Hospital satisfaction comparisons.
- Patient recommendation responses.
- Resource data-quality issues.

SQL results were compared with the Python analysis to verify consistency.

## 10. Streamlit Dashboard

A Streamlit dashboard was developed to present the analytical findings.

The dashboard includes:

- Appointment KPIs.
- Department-wise and specialty-wise no-show charts.
- Patient satisfaction comparisons.
- Resource data-quality findings.
- Interactive department, specialty, and insurance filters.

### Run the Dashboard

From the repository root, execute:

```bash
streamlit run "Pristyn-Care-Health/dashboard/app.py"
```

## 11. Reports and Documentation

The project includes:

- `reports/executive_summary.md`
- `reports/ab_test_proposals.md`
- `docs/SQL_ANALYSIS.md`

These documents describe the findings, recommendations, proposed experiments, and SQL analysis.

## 12. Tools and Technologies

- Python
- Pandas
- SQLite
- SQL
- Streamlit
- Plotly
- Git and GitHub
- VS Code

## 13. Project Limitations

The available datasets support appointment, patient satisfaction, and resource data-quality analysis.

However, they do not contain all seven stages of the required patient funnel:

1. Ad click
2. Enquiry
3. Consultation
4. Diagnostics
5. Booking
6. Surgery
7. Follow-up

Therefore, actual funnel conversion rates, leakage percentages, and the requested 5% conversion-lift revenue impact cannot be calculated using the available data.

Additional patient journey stage counts and revenue information are required.

The appointment dataset and Sunrise satisfaction/resource datasets should not be assumed to represent the same organisation or a joined patient journey.

## 14. Data Privacy

Raw healthcare CSV files and the SQLite database are excluded from Git using `.gitignore`.

These files should remain private unless sharing permission and applicable data-protection requirements have been confirmed.

## 15. Conclusion

The project identified appointment no-show patterns, patient satisfaction trends, and important resource data-quality issues.

Python, SQL, and Streamlit were used to analyse and present the available data. The findings provide a starting point for improving appointment management and patient experience.

Further patient journey data, revenue information, and validated resource records are required to complete the full business analysis.
