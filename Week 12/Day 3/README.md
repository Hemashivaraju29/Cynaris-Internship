# Week 12 - Day 3: Security Audit on Data Platform

## 1. Project Objective

The objective of this task is to conduct a defensive security audit of a local data platform. The audit checks potential sensitive-data exposure, credential security, data classification and security-control gaps.

## 2. Dataset

- **Dataset:** Sales dataset
- **Source:** `Week 05/Day 4/data_100k.csv`
- **Rows scanned:** 100,000
- **Columns scanned:** 8
- **Missing values:** Previously verified as zero

The audit reads the dataset locally and does not intentionally include sensitive values in its reports.

## 3. Project Structure

```text
Week 12/
└── Day 3/
    ├── docs/
    ├── outputs/
    │   ├── security_audit_report.csv
    │   └── security_audit_summary.json
    ├── src/
    │   └── security_audit.py
    ├── tests/
    │   └── test_security_audit.py
    ├── README.md
    └── requirements.txt
```

## 4. Security Audit Checks

### Data classification

- Identifies potential direct personal identifiers.
- Identifies pseudonymous or indirect identifiers such as `customer_id`.
- Classifies general business-data columns.

### Sensitive-data detection

Checks for patterns resembling:

- Email addresses
- Aadhaar numbers
- PAN numbers
- Indian mobile numbers in relevant columns

The scanner records matching counts and column names, not the actual matched values.

### Credential security

Checks eligible repository text files for supported patterns such as:

- Private-key headers
- AWS access-key identifiers
- GitHub token formats
- Hardcoded password, API-key and secret assignments

Local `.env` and `.env.*` files are excluded from scanning and must remain outside Git.

### Data integrity

Calculates the SHA-256 checksum of the input dataset for integrity tracking.

### Platform-control review

Identifies security controls requiring manual verification:

- Least-privilege database permissions
- Encryption
- Multi-factor authentication
- Audit logging
- Backup protection
- Data-retention policies

## 5. Initial Security Finding and Remediation

The initial audit detected a potential hardcoded database password in:

`Week 06/Day 1/vanna_sql_analyst.py`

The finding was treated as a genuine credential exposure.

Remediation performed:

1. Changed the original MySQL root password.
2. Created a dedicated MySQL application account named `vanna_analyst`.
3. Configured the account with SELECT-only permission on `sales_db`.
4. Replaced hardcoded database credentials in the Python application with environment-variable configuration.
5. Stored the replacement application credentials in the local `.env` file.
6. Excluded `.env` from Git and from the local repository secret-pattern scan.
7. Verified successful authentication as `vanna_analyst@localhost`.
8. Successfully executed a read-only query against the `sales` table.

The original credential should be considered invalidated. The historical Git commit contents have not been rewritten or independently audited.

## 6. Final Security Audit Results

| Metric                  |  Result |
| ----------------------- | ------: |
| Dataset rows scanned    | 100,000 |
| Dataset columns scanned |       8 |
| Total audit checks      |      12 |
| PASS                    |      10 |
| FAIL                    |       0 |
| REVIEW REQUIRED         |       2 |

### Remaining findings

**Finding 1: Customer identifier**

`customer_id` is classified as a pseudonymous or indirect identifier. Access should be restricted, and potential re-identification risks should be assessed.

**Finding 2: Platform security controls**

Encryption, MFA, audit logging, backup protection and retention policies require further verification with the platform administrator.

The dedicated MySQL application's SELECT-only database permission was verified separately.

## 7. Automated Testing

Pytest was used to test the security-audit functionality.

**Test result: 7 passed**

Tests cover:

- Direct-identifier classification.
- Indirect-identifier classification.
- General business-data classification.
- Sensitive email-pattern detection.
- Secret-pattern detection without exposing matched values.
- Excluding `.env` from repository scanning.
- SHA-256 checksum generation.

## 8. Installation and Execution

Install the project dependencies:

```bash
pip install -r "Week 12/Day 3/requirements.txt"
```

Run the audit:

```bash
python "Week 12/Day 3/src/security_audit.py"
```

Run automated tests:

```bash
python -m pytest "Week 12/Day 3/tests" -v
```

## 9. Tools and Technologies

- Python 3.11
- Pandas
- Pytest
- Regular Expressions
- SHA-256 / Hashlib
- python-dotenv
- MySQL 8.0.46
- MySQL Workbench
- CSV and JSON
- VS Code
- PowerShell
- Git and GitHub

## 10. Audit Limitations

This is a local, pattern-based security audit. It is not a penetration test or a complete security certification.

- Pattern matching may produce false positives or miss unrecognised formats.
- The scanner does not inspect Git commit history.
- Excluded `.env` files are not scanned; their protection depends on local file security and Git exclusion.
- Database encryption, MFA, audit logging, backups and retention require administrator verification.
- A PASS result does not prove the absence of every security weakness.

## 11. Conclusion

The security audit identified and supported remediation of a hardcoded database credential, introduced a dedicated read-only MySQL application account, and generated structured audit reports.

The final run recorded 10 PASS, 0 FAIL and 2 REVIEW REQUIRED results. All seven automated tests passed.

The remaining review items identify controls that need further verification rather than being reported as completed security checks.
