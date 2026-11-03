# SQL Analysis Documentation

## 1. Objective

SQL was used to analyse healthcare appointments, patient satisfaction, and hospital resource utilisation data.

## 2. Database Setup

- Database: SQLite
- Database name: `pristyn_healthcare.db`
- Total records imported: 3,000

## 3. Database Tables

| Table                   | Records |
| ----------------------- | ------: |
| healthcare_appointments |   2,000 |
| patient_satisfaction    |     600 |
| resource_utilisation    |     400 |

## 4. Appointment Analysis

- Total appointments: 2,000
- Attended appointments: 1,676
- No-show appointments: 324
- Overall no-show rate: 16.20%
- Highest department no-show rate: Emergency (18.00%)
- Highest specialty no-show rate: General Medicine (22.50%)

## 5. Patient Satisfaction Analysis

- Average doctor rating: 2.92
- Average nurse rating: 2.96
- Average cleanliness rating: 3.04
- Average billing clarity rating: 2.93
- Average overall satisfaction: 3.04
- Highest hospital satisfaction: Sunrise South (3.37)
- Lowest hospital satisfaction: Sunrise East (2.81)

## 6. Patient Recommendation

- Yes: 351
- No: 134
- Maybe: 115

## 7. Resource Data Quality

The SQL validation identified:

- Invalid bed records: 175
- Invalid ICU records: 175
- Invalid surgery records: 182

These records require investigation before calculating reliable resource utilisation metrics. Issue counts may overlap.

## 8. Conclusion

SQL successfully imported and analysed all three datasets. Appointment and satisfaction results were consistent with the Python analysis. Resource data-quality issues were identified for further investigation.

## 9. Limitations

The available datasets do not contain the complete seven-stage Pristyn Care patient journey or the revenue information required to calculate actual funnel conversion rates and revenue impact. The Sunrise datasets should not be assumed to represent Pristyn Care operations.
