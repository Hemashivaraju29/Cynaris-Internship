# W10D3 – Anomaly Detection Using Isolation Forest and Statistical Methods

## 1. Project Overview

This project focuses on identifying unusual observations in historical Indian stock market data using two anomaly detection techniques: the Statistical Z-Score method and Isolation Forest.

The analysis uses Reliance stock closing prices from the Nifty 500 dataset.

## 2. Objectives

- Understand anomaly detection techniques.
- Identify unusual stock price observations.
- Apply statistical methods using Z-Score.
- Implement machine learning-based detection using Isolation Forest.
- Compare the results of both methods.
- Visualize detected anomalies.

## 3. Dataset Details

**Dataset:** nifty500_combined_eda.csv

**Selected Company:** Reliance

- Total records: 2,465
- Columns used: Date and Close
- Date range: 2012–2021
- Missing or invalid dates and closing prices were removed.

## 4. Methodology

### A. Data Preparation

- Loaded the Nifty 500 dataset using Pandas.
- Filtered records for Reliance.
- Converted Date and Close columns into appropriate data types.
- Removed missing and invalid records.
- Sorted records by date.

### B. Statistical Method – Z-Score

The Z-Score method measures how far a value is from the average.

- Calculated the mean and standard deviation.
- Calculated the Z-Score for each closing price.
- Used an absolute Z-Score greater than 3 as the default anomaly threshold.
- Marked unusual observations as statistical anomalies.

### C. Isolation Forest

Isolation Forest is a machine learning algorithm that identifies unusual observations by isolating data points.

- Applied the Isolation Forest algorithm.
- Used a contamination setting of 2%.
- Set `random_state=42` for reproducible results.
- Marked predictions of -1 as anomalies.

### D. Comparison

Compared the anomalies identified by both methods and identified observations flagged by both.

## 5. Results

| Detection Method | Anomalies |
| ---------------- | --------: |
| Z-Score          |         0 |
| Isolation Forest |        50 |
| Both Methods     |         0 |

The Z-Score method did not identify any observations beyond the selected threshold of 3 standard deviations.

Isolation Forest identified 50 unusual observations using the 2% contamination setting.

The two methods use different approaches, so their results can differ.

## 6. Output Files

The project generates the following files inside the output folder:

- `anomaly_detection_results.csv` – Detailed detection results.
- `anomaly_summary.csv` – Summary of detected anomalies.
- `anomaly_detection_plot.png` – Visualization of stock prices and detected anomalies.

## 7. Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Pytest

## 8. Project Structure

```text
Week 10/
└── Day 3/
    ├── anomaly_detection.py
    ├── README.md
    ├── requirements.txt
    ├── .gitignore
    ├── tests/
    │   └── test_anomaly_detection.py
    └── output/
```

## 9. How to Run

Install the dependencies:

```bash
pip install -r "Week 10/Day 3/requirements.txt"
```

Run the anomaly detection script from the repository root:

```bash
python "Week 10/Day 3/anomaly_detection.py"
```

Run automated tests:

```bash
python -m pytest "Week 10/Day 3/tests/test_anomaly_detection.py" -v
```

## 10. Testing

Five automated tests were executed successfully.

**Test Result:** 5 passed.

The tests validate:

- Data loading and preparation.
- Reliance record count.
- Statistical anomaly detection.
- Isolation Forest detection.
- Handling of constant values.

## 11. Limitations

- The analysis uses only Reliance closing prices.
- The Z-Score method may not identify unusual values in all types of data distributions.
- Isolation Forest's contamination parameter influences the number of detected anomalies.
- Detected anomalies are unusual observations, not necessarily errors or fraudulent activities.
- Further investigation is required before making financial decisions.

## 12. Conclusion

The project successfully implemented two anomaly detection techniques on Reliance stock market data. Isolation Forest identified 50 unusual observations, while the Z-Score method identified none using the default threshold. Comparing both methods helps understand how statistical and machine learning techniques can identify unusual patterns in financial data.
