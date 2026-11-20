# Week 12 – Project Architecture

## 1. Architecture Overview

The Week 12 project consists of two main modules:

1. Performance Optimisation using DuckDB and Query Caching.
2. Security Audit on Data Platform.

Both modules use Python for processing, validation and report generation.

## 2. Performance Optimisation Architecture

```text
        Sales Dataset (100K Rows)
                  |
          +-------+-------+
          |               |
       DuckDB           Pandas
          |               |
      SQL Queries     Data Analysis
          |               |
          +-------+-------+
                  |
          Performance Benchmark
                  |
          Query Result Caching
                  |
          +-------+-------+
          |               |
     Analytical CSV    Benchmark CSV
        Outputs           Output
```

### Components

- **Source:** Sales CSV dataset.
- **DuckDB:** In-process analytical SQL execution.
- **Pandas:** Data manipulation and performance comparison.
- **SQL queries:** Total sales, category performance, city performance, top products and payment analysis.
- **Query cache:** In-memory storage of reusable query results.
- **Outputs:** Analytical CSV files and benchmark results.

## 3. Security Audit Architecture

```text
          Sales Dataset
                |
          Python Audit
                |
       +--------+---------+
       |        |         |
  Data       Sensitive   Integrity
Classification Pattern   Check
       |      Detection  (SHA-256)
       |        |         |
       +--------+---------+
                |
        Repository Scan
                |
       Security Findings
                |
        +-------+-------+
        |               |
      CSV Report    JSON Summary
```

### Components

- **Pandas:** Dataset inspection and classification.
- **Regular Expressions:** Sensitive-data and credential-pattern detection.
- **Hashlib:** SHA-256 checksum calculation.
- **Repository scanner:** Detection of supported secret patterns in eligible files.
- **Outputs:** Security audit report and summary.

## 4. MySQL Credential Security Architecture

```text
       Python Vanna Application
                 |
             python-dotenv
                 |
              .env File
                 |
          MySQL Credentials
                 |
          MySQL Server 8.0
                 |
             sales_db
                 |
          vanna_analyst
                 |
          SELECT Permission
```

The application uses environment variables instead of hardcoded database credentials.

The dedicated `vanna_analyst` account has read-only access to the `sales_db` database.

## 5. Testing Architecture

```text
       Python Source Files
                |
              Pytest
                |
        Automated Test Cases
                |
       +--------+--------+
       |                 |
   W12D2 Tests       W12D3 Tests
       |                 |
    6 Passed          7 Passed
       |                 |
       +--------+--------+
                |
        13 Tests Passed
```

## 6. Technologies

- Python 3.11
- DuckDB
- Pandas
- SQL
- MySQL 8.0
- Pytest
- Regular Expressions
- Hashlib
- python-dotenv
- CSV and JSON
- Git and GitHub

## 7. Architecture Summary

The architecture separates analytical processing, performance benchmarking, security auditing and database access.

Each module produces structured outputs that support validation, reporting, project handover and final demonstration.
