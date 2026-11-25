# Pristyn Care Health – Healthcare Data Analytics

## Executive Brief

### 1. Project Overview

The objective of this project is to analyse healthcare appointment data, patient satisfaction, and hospital resource utilisation to identify operational challenges and opportunities for improvement.

Python, SQL, statistical analysis, and a Streamlit dashboard were used to examine the available datasets and present actionable findings.

### 2. Key Findings

**Appointment Analysis**

A total of 2,000 healthcare appointments were analysed.

| Metric                | Result |
| --------------------- | -----: |
| Total appointments    |  2,000 |
| Attended appointments |  1,676 |
| No-show appointments  |    324 |
| Overall no-show rate  | 16.20% |

General Medicine recorded the highest specialty-level no-show rate at 22.50%, followed by Dermatology at 20.46%.

Emergency had the highest department-level no-show rate at 18.00%.

These findings suggest that appointment reminder and confirmation processes should be reviewed, particularly for specialties with higher observed no-show rates.

**Statistical Analysis**

Chi-square tests were conducted to examine associations between appointment no-show status and five factors.

Specialty showed a statistically significant association with no-show status (p = 0.000031). Department, patient age group, insurance type, and booking hour did not show statistically significant associations at the 5% level.

The specialty result remains significant after a Holm adjustment based on the five reported p-values (adjusted p approximately 0.000155). Expected cell counts should still be checked. These results show association, not causation.

**Patient Satisfaction Analysis**

A total of 600 patient satisfaction surveys were analysed.

| Metric                         |        Result |
| ------------------------------ | ------------: |
| Average doctor rating          |      2.92 / 5 |
| Average nurse rating           |      2.96 / 5 |
| Average cleanliness rating     |      3.04 / 5 |
| Average billing clarity rating |      2.93 / 5 |
| Average overall satisfaction   |      3.04 / 5 |
| Average waiting time           | 91.43 minutes |

Sunrise South recorded the highest average satisfaction at 3.37, while Sunrise East recorded the lowest at 2.81.

The results indicate opportunities to review billing communication, waiting times, and patient experience, particularly at Sunrise East.

**Resource Data Quality**

The resource utilisation dataset contained 400 records. A total of 337 records (84.25%) had at least one validation issue.

The identified issues included:

- Occupied beds exceeding total beds.
- ICU occupied beds exceeding available ICU beds.
- Completed surgeries exceeding scheduled surgeries.

These records require investigation. Resource utilisation KPIs should not be used for operational decisions until the source data and reporting definitions are verified.

### 3. Business Recommendations

1. **Improve appointment attendance:** Introduce or review SMS and WhatsApp reminders and appointment confirmation processes.
2. **Investigate specialty-level no-shows:** Examine possible reasons for higher no-show rates in General Medicine and Dermatology.
3. **Improve patient experience:** Review billing explanations, communication, and waiting-time management.
4. **Focus on lower satisfaction:** Investigate patient feedback and service processes at Sunrise East.
5. **Improve data quality:** Validate bed capacity, ICU occupancy, and surgery records before using resource KPIs.

### 4. Proposed A/B Testing

Four experiments are proposed for future evaluation:

- Appointment reminder messages versus the existing reminder process.
- Additional appointment confirmation for General Medicine.
- Clearer, itemised billing explanations.
- Structured patient follow-up at Sunrise East.

These are proposed experiments, not completed tests. Each should use a defined study period, appropriate randomisation, and preselected success metrics.

### 5. Project Limitations

The available datasets support appointment, satisfaction, and resource data-quality analysis. However, they do not contain a complete seven-stage patient journey:

1. Ad click
2. Enquiry
3. Consultation
4. Diagnostics
5. Booking
6. Surgery
7. Follow-up

Consequently, actual funnel conversion rates, leakage percentages, and the requested 5% conversion-lift revenue impact cannot be calculated reliably.

Additional stage-level patient journey counts and revenue information are required.

The appointment dataset and Sunrise satisfaction/resource datasets should not be assumed to represent the same organisation or a joined patient journey.

### 6. Conclusion

The analysis identified a 16.20% appointment no-show rate, differences in patient satisfaction across hospitals, and substantial resource data-quality concerns.

The findings provide a starting point for improving appointment management and patient experience. Further data collection, validation, and controlled experiments are recommended before making wider operational or financial conclusions.

**Prepared as a data analytics project using the datasets available for analysis.**
