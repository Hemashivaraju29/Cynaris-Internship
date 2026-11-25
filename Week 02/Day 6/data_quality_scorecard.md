# Data Quality Scorecard — Week 2 Day 6

## Dataset

**Dataset:** Sales Data  
**Source:** Week 01/Day 5/sales_cleaned.csv  
**Consumer:** BI Dashboard  
**Assessment:** Great Expectations + DAMA data quality dimensions

---

## 1. DAMA Data Quality Assessment

| Dimension    | Score | Assessment                                                                                                    |
| ------------ | ----: | ------------------------------------------------------------------------------------------------------------- |
| Accuracy     |   4/5 | Values are reasonable for the sample sales data, but source-system accuracy cannot be independently verified. |
| Completeness |   4/5 | Required fields are populated in the clean dataset; missing-value checks are included in GX.                  |
| Consistency  |   4/5 | Categories and payment methods follow standard values after cleaning.                                         |
| Timeliness   |   3/5 | The dataset has no transaction timestamp, so freshness cannot be fully measured.                              |
| Validity     |   4/5 | Numeric and categorical fields follow defined validation rules.                                               |
| Uniqueness   |   4/5 | sale_id is expected to be unique and is validated using Great Expectations.                                   |

**Overall Score: 23/30 — Good**

---

## 2. Great Expectations Results

Eight expectations were created and tested.

- `sale_id` must not be null — PASS
- `sale_id` must be unique — FAIL on intentionally corrupted data
- `customer_name` must not be null — FAIL on intentionally corrupted data
- `amount` must not be null — PASS
- `amount` must be greater than zero — FAIL on intentionally corrupted data
- `quantity` must be greater than zero — PASS
- `category` must contain approved values — PASS
- `payment_method` must contain approved values — PASS

**Result:** Great Expectations successfully detected all 3 intentionally introduced data-quality errors.

---

## 3. PII Assessment

| Column         | Classification                        | Risk   | Recommended Protection                      |
| -------------- | ------------------------------------- | ------ | ------------------------------------------- |
| customer_name  | Direct PII                            | High   | Tokenisation or masking                     |
| sale_id        | Identifier / pseudonymous             | Low    | Keep internal; avoid exposing unnecessarily |
| city           | Location attribute / quasi-identifier | Medium | Aggregate to region where possible          |
| product        | Non-PII                               | Low    | No masking required                         |
| category       | Non-PII                               | Low    | No masking required                         |
| quantity       | Non-PII                               | Low    | No masking required                         |
| amount         | Transaction data                      | Medium | Restrict access; aggregate for dashboards   |
| payment_method | Non-PII                               | Low    | No masking required                         |

### Recommended PII Strategy

`customer_name` should be tokenised before data is exposed to the BI dashboard. The dashboard should use a stable customer token instead of the actual customer name.

Example:

`Anil → CUST_001`

Direct customer names should remain restricted to authorised users only.

---

## 4. Improvement Recommendations

1. Add a `sale_date` or timestamp column to measure data freshness and improve the Timeliness score.
2. Enforce `sale_id` uniqueness at the source database level.
3. Run Great Expectations validation automatically before dashboard refreshes.
4. Reject or quarantine records containing invalid amounts, missing required fields, or duplicate IDs.
5. Tokenise customer names before sharing data with BI tools.
6. Monitor data-quality scores regularly and track failed validation checks over time.

---

## 5. Final Assessment

The dataset has **good overall data quality (23/30)** based on the six DAMA dimensions.

The validation process demonstrated that automated Great Expectations checks can identify duplicate IDs, missing customer names, and invalid negative transaction amounts before the data reaches the BI dashboard.
