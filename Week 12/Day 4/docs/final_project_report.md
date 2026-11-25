# Final Project Report – Week 12

## 1. Executive Summary

This report consolidates the Week 12 Data Analyst Internship activities, covering performance optimisation, data-platform security auditing, automated testing and project documentation.

The work involved using DuckDB for analytical SQL queries and query caching, comparing analytical performance with Pandas, and developing a Python-based security audit for a sales data platform.

The objective was to improve query performance, identify potential data-security risks and prepare reproducible technical documentation.

## 2. Project Objectives

- Implement efficient analytical queries using DuckDB.
- Develop reusable SQL query execution and caching.
- Compare DuckDB and Pandas query performance.
- Identify possible sensitive-data exposure.
- Detect potential hardcoded credentials in repository files.
- Implement data classification and integrity checks.
- Apply least-privilege database access.
- Prepare automated tests and final project documentation.

## 3. Technologies Used

| Technology          | Purpose                                         |
| ------------------- | ----------------------------------------------- |
| Python 3.11         | Application development and audit automation    |
| DuckDB              | In-process SQL analytics                        |
| Pandas              | Data manipulation and performance comparison    |
| SQL                 | Analytical queries and database access          |
| MySQL 8.0           | Relational database management                  |
| Pytest              | Automated testing                               |
| Regular Expressions | Sensitive-data and credential-pattern detection |
| Hashlib             | SHA-256 checksum generation                     |
| python-dotenv       | Environment-variable configuration              |
| CSV and JSON        | Data and report storage                         |
| Git and GitHub      | Version control and collaboration               |

## 4. Week 12 Day 2 – Performance Optimisation

### 4.1 Objective

Improve analytical query execution and explore query-result caching using DuckDB.

### 4.2 Implementation

- Configured DuckDB for in-process analytical processing.
- Loaded the 100,000-row sales dataset.
- Developed five analytical SQL queries.
- Created a reusable SQL-to-Pandas DataFrame function.
- Implemented in-memory SQL query-result caching.
- Benchmarked DuckDB against Pandas using three equivalent analytical queries.
- Generated analytical and benchmark CSV files.

### 4.3 Analytical Outputs

The following outputs were generated:

1. `total_sales.csv`
2. `category_performance.csv`
3. `city_performance.csv`
4. `top_products.csv`
5. `payment_analysis.csv`
6. `performance_benchmark.csv`

### 4.4 Performance Findings

The benchmark observations were:

- Pandas performed faster for city and category revenue aggregations.
- DuckDB performed approximately 1.35 times faster for payment performance.

The results demonstrate that query-engine performance depends on the analytical operation and workload.

### 4.5 Testing

- Automated tests executed: 6
- Tests passed: 6

## 5. Week 12 Day 3 – Security Audit

### 5.1 Objective

Develop a defensive security-audit system to identify potential sensitive-data exposure, credential risks and security-control gaps in a local data platform.

### 5.2 Dataset

| Property        | Value                       |
| --------------- | --------------------------- |
| Dataset         | Sales dataset               |
| Rows scanned    | 100,000                     |
| Columns scanned | 8                           |
| Source          | Week 05 Day 4 sales dataset |

### 5.3 Security Checks

**Data classification**

Identified potential direct identifiers, pseudonymous identifiers and general business-data columns.

**Sensitive-data detection**

Implemented pattern detection for:

- Email addresses
- Aadhaar-like numbers
- PAN-like numbers
- Indian mobile numbers in relevant columns

**Credential security**

Implemented repository scanning for potential:

- Hardcoded passwords
- API keys and access tokens
- Private-key headers
- Other supported secret patterns

The scanner records finding metadata rather than matched secret values. Local environment files are excluded from scanning.

**Data integrity**

Implemented SHA-256 checksum generation to support dataset integrity tracking.

**Platform security review**

Identified the need to manually verify:

- Access permissions
- Encryption
- Multi-factor authentication
- Audit logging
- Backup protection
- Data-retention policies

### 5.4 MySQL Credential Remediation

During the audit, a hardcoded MySQL password was detected in the existing Vanna SQL Analyst application.

The following remediation was performed:

1. Changed the original MySQL root password.
2. Created a dedicated application account named `vanna_analyst`.
3. Granted SELECT-only access to the `sales_db` database.
4. Moved application credentials into the local `.env` file.
5. Updated the Python application to retrieve credentials using environment variables.
6. Excluded `.env` from Git.
7. Verified successful authentication as `vanna_analyst@localhost`.
8. Successfully executed a read-only query against the sales table.

**Security limitation:** The earlier credential may remain in historical Git commits. Credential rotation invalidates the old password but does not remove its historical copy. Repository-history cleanup remains a separate follow-up.

### 5.5 Final Security Audit Results

| Audit status    | Count |
| --------------- | ----: |
| PASS            |    10 |
| FAIL            |     0 |
| REVIEW REQUIRED |     2 |
| Total checks    |    12 |

Remaining review items:

1. `customer_id` may create a re-identification risk when combined with other information.
2. Platform-level encryption, MFA, audit logging, backup protection and retention require manual verification.

### 5.6 Generated Reports

- `security_audit_report.csv`
- `security_audit_summary.json`

### 5.7 Automated Testing

- Automated tests executed: 7
- Tests passed: 7

## 6. Consolidated Testing Results

| Project module           | Tests executed | Tests passed |
| ------------------------ | -------------: | -----------: |
| W12D2 – DuckDB analytics |              6 |            6 |
| W12D3 – Security audit   |              7 |            7 |
| Total                    |             13 |           13 |

All recorded automated tests passed successfully.

## 7. Project Architecture

The project follows a modular structure:

- Data inputs provide the sales dataset.
- Python scripts handle analytics and security checks.
- DuckDB executes analytical SQL queries.
- Pandas supports data processing and comparison.
- Query caching stores reusable query results in memory.
- MySQL manages relational sales data and restricted database access.
- Audit scripts produce security findings.
- CSV and JSON files store generated outputs.
- Pytest validates the implemented functionality.

## 8. Limitations

- Benchmark performance depends on dataset size, hardware and query workload.
- Query caching is in-memory and does not provide persistent caching.
- Pattern-based security scanning may produce false positives or miss unrecognised formats.
- The security audit does not constitute a complete penetration test.
- Local repository scans do not automatically inspect historical Git commits.
- Some platform-level security controls require administrator verification.
- Repository-history credential cleanup remains outstanding.

## 9. Future Improvements

- Evaluate query performance using larger datasets.
- Explore persistent query caching and cache invalidation.
- Expand data-classification rules.
- Integrate automated secret scanning into the Git workflow.
- Verify encryption, MFA and database audit logging.
- Improve monitoring and alerting for suspicious access.
- Complete repository-history remediation with mentor approval.

## 10. Conclusion

Week 12 activities provided practical experience in analytical performance optimisation, SQL query execution, caching, database security and automated auditing.

DuckDB and Pandas were compared through benchmarking, while the security-audit implementation identified potential data and credential risks. A dedicated read-only MySQL account was configured, application credentials were moved to environment variables, and the audit generated structured reports.

A total of 13 automated tests passed across the two completed modules.

The final documentation and demonstration materials consolidate the implementation, results, testing evidence, limitations and recommendations for project handover and final assessment.
