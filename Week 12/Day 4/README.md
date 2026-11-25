# Week 12 – Final Project Documentation and Demo Preparation

## 1. Project Overview

This project consolidates the Week 12 Data Analyst Internship activities, focusing on performance optimisation, data-platform security and final project documentation.

### Main Objectives

- Improve analytical query performance using DuckDB.
- Implement reusable SQL query execution and caching.
- Compare DuckDB and Pandas query performance.
- Conduct a security audit of a sales data platform.
- Identify potential sensitive-data exposure and credential risks.
- Prepare technical documentation and a reproducible project demonstration.

## 2. Project Modules

### Week 12 Day 2 – Performance Optimisation with DuckDB and Query Caching

Activities completed:

- Configured DuckDB for in-process SQL analytics.
- Implemented five analytical queries.
- Developed a reusable SQL-to-Pandas DataFrame function.
- Implemented in-memory query-result caching.
- Benchmarked DuckDB against Pandas.
- Generated analytical and benchmark CSV outputs.
- Completed 6 automated tests.

Benchmark observations:

- Pandas performed faster for city and category revenue aggregations.
- DuckDB performed approximately 1.35 times faster for payment performance.

### Week 12 Day 3 – Security Audit on Data Platform

Activities completed:

- Audited a 100,000-row sales dataset with 8 columns.
- Implemented data classification.
- Detected patterns resembling emails, Aadhaar numbers, PAN numbers and Indian mobile numbers.
- Implemented repository secret-pattern scanning.
- Added SHA-256 checksum generation.
- Generated CSV and JSON audit reports.
- Configured a dedicated read-only MySQL application account.
- Replaced hardcoded database credentials with environment-variable configuration.
- Completed 7 automated tests.

Final security audit results:

| Metric          | Result |
| --------------- | -----: |
| Total checks    |     12 |
| PASS            |     10 |
| FAIL            |      0 |
| REVIEW REQUIRED |      2 |

Remaining review findings:

1. Customer identifier re-identification risk.
2. Manual verification of encryption, MFA, audit logging, backups and data retention.

## 3. Technologies and Tools

- Python 3.11
- DuckDB
- Pandas
- SQL
- MySQL 8.0
- MySQL Workbench
- Pytest
- Regular Expressions
- Hashlib / SHA-256
- python-dotenv
- CSV and JSON
- VS Code
- PowerShell
- Git and GitHub

## 4. Project Results

### Performance Optimisation

- Five analytical queries implemented.
- Query-result caching implemented.
- DuckDB and Pandas performance compared.
- Six automated tests completed successfully.

### Security Audit

- 100,000 rows and 8 columns scanned.
- 10 checks passed.
- No potential secret-pattern findings in the final scan.
- Two findings retained for manual review.
- Seven automated tests passed.

## 5. Security Considerations

- MySQL application credentials are stored in a local `.env` file.
- The `.env` file is excluded from Git.
- A dedicated `vanna_analyst` account uses SELECT-only access to `sales_db`.
- The application no longer uses hardcoded root credentials.
- Audit reports do not intentionally expose detected secret values.
- Historical Git commits may still contain the previously exposed credential. Credential rotation was performed; repository-history cleanup remains a separate security follow-up.

## 6. Documentation and Demo Structure

```text
Week 12/
├── Day 2/
│   ├── README.md
│   ├── src/
│   ├── tests/
│   └── outputs/
├── Day 3/
│   ├── README.md
│   ├── src/
│   ├── tests/
│   └── outputs/
└── Day 4/
    ├── README.md
    ├── docs/
    ├── demo/
    └── outputs/
```

## 7. Conclusion

Week 12 activities covered performance optimisation, SQL query caching, data-platform security auditing, automated testing and technical documentation.

The completed work demonstrates practical experience with Python, SQL analytics, DuckDB, Pandas, MySQL, security checks, performance benchmarking, Git version control and project documentation.

The final demonstration will present the implementation, execution process, test results, analytical outputs, security findings and remaining recommendations.
