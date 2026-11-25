# Week 12 – Final Project Demonstration Script

## 1. Introduction

Good morning everyone.

Today, I am presenting my Week 12 Data Analyst Internship work, which focuses on performance optimisation, data-platform security and final project documentation.

The project consists of two major modules:

1. DuckDB Analytics and Query Caching.
2. Security Audit on Data Platform.

The objective was to improve analytical query execution, implement reusable query caching, identify potential security risks and generate structured reports.

## 2. Demonstration – Day 2: DuckDB Analytics

### Step 1: Explain the dataset

I used a 100,000-row sales dataset to demonstrate analytical query processing and performance comparison.

### Step 2: Explain implementation

I implemented five analytical SQL queries:

- Total sales
- Category performance
- City performance
- Top products
- Payment analysis

I also developed:

- A reusable SQL-to-Pandas DataFrame function.
- An in-memory query-result caching mechanism.
- A benchmarking script comparing DuckDB and Pandas.

### Step 3: Run the benchmark

Execute:

```powershell
python "Week 12\Day 2\src\benchmark.py"
```

Show the generated benchmark results:

```powershell
Import-Csv "Week 12\Day 2\outputs\performance_benchmark.csv" |
Format-Table -AutoSize
```

### Step 4: Explain benchmark findings

The benchmark showed that:

- Pandas performed faster for city and category revenue aggregations.
- DuckDB performed approximately 1.35 times faster for payment performance.

This demonstrated that performance depends on the query workload and analytical operation.

### Step 5: Show analytical outputs

Open the following files:

- `total_sales.csv`
- `category_performance.csv`
- `city_performance.csv`
- `top_products.csv`
- `payment_analysis.csv`

## 3. Demonstration – Day 3: Security Audit

### Step 1: Explain the objective

The objective was to identify potential sensitive-data exposure, hardcoded credentials, data-classification risks and security-control gaps.

### Step 2: Run the security audit

Execute:

```powershell
python "Week 12\Day 3\src\security_audit.py"
```

Explain that the script scans a 100,000-row sales dataset containing 8 columns.

### Step 3: Show security audit results

Display the final report:

```powershell
Import-Csv "Week 12\Day 3\outputs\security_audit_report.csv" |
Format-Table check_id, category, status, severity -AutoSize
```

Explain the final results:

| Status          | Count |
| --------------- | ----: |
| PASS            |    10 |
| FAIL            |     0 |
| REVIEW REQUIRED |     2 |

### Step 4: Explain credential remediation

During the audit, a hardcoded MySQL password was identified in an existing Python application.

Explain the remediation:

- Changed the original database root password.
- Created a dedicated MySQL application user.
- Granted SELECT-only access to the sales database.
- Moved application credentials into environment variables.
- Excluded `.env` from Git.

Demonstrate the verified database account:

```sql
SELECT CURRENT_USER();
SELECT COUNT(*) AS sales_rows FROM sales;
```

The authenticated application account was `vanna_analyst@localhost`, and the sales query returned 10 rows.

Never display the password or open the `.env` file during the presentation.

### Step 5: Explain remaining findings

Two findings require further review:

1. Customer identifiers may create re-identification risks.
2. Encryption, MFA, audit logging, backup protection and data retention require platform-administrator verification.

Explain that these items were not incorrectly marked as passed.

## 4. Automated Testing Demonstration

### Day 2 tests

Execute:

```powershell
python -m pytest "Week 12\Day 2\tests" -v
```

Expected result: 6 tests passed.

### Day 3 tests

Execute:

```powershell
python -m pytest "Week 12\Day 3\tests" -v
```

Expected result: 7 tests passed.

### Consolidated result

| Module           | Tests passed |
| ---------------- | -----------: |
| DuckDB analytics |            6 |
| Security audit   |            7 |
| Total            |           13 |

## 5. Tools and Technologies

The project used:

- Python
- DuckDB
- Pandas
- SQL
- MySQL
- Pytest
- Regular Expressions
- Hashlib
- python-dotenv
- VS Code
- PowerShell
- Git and GitHub

## 6. Conclusion

To conclude, Week 12 helped me gain practical experience in analytical query optimisation, SQL query caching, performance benchmarking, data security auditing, credential management and automated testing.

I also prepared technical documentation, generated structured reports and maintained the project using Git and GitHub.

Thank you.
