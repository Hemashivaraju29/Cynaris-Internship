
"""Defensive security audit for the local sales data platform."""

import hashlib
import json
import re
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATASET_PATH = (
    PROJECT_ROOT / "Week 05" / "Day 4" / "data_100k.csv"
)
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "outputs"

DIRECT_ID_PATTERN = re.compile(
    r"(^|_)(email|e_mail|phone|mobile|aadhaar|aadhar|pan|"
    r"passport|dob|date_of_birth|address|full_name|first_name|"
    r"last_name)(_|$)",
    re.IGNORECASE,
)

INDIRECT_ID_PATTERN = re.compile(
    r"(^|_)(customer|user|account|device|session)_?id($|_)",
    re.IGNORECASE,
)

VALUE_PATTERNS = {
    "email_like": re.compile(
        r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
        re.IGNORECASE,
    ),
    "aadhaar_like": re.compile(
        r"(?<!\d)[2-9]\d{3}[\s-]?\d{4}[\s-]?\d{4}(?!\d)"
    ),
    "pan_like": re.compile(
        r"\b[A-Z]{5}\d{4}[A-Z]\b",
        re.IGNORECASE,
    ),
    "indian_mobile_like": re.compile(
        r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)"
    ),
}

SECRET_PATTERNS = {
    "private_key_header": re.compile(
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
    ),
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "credential_assignment": re.compile(
        r"""(?i)\b(?:password|passwd|client_secret|api_key|"""
        r"""access_token|secret_key)\b\s*[:=]\s*"""
        r"""['"][^'"\r\n]{8,}['"]"""
    ),
}

SCANNED_EXTENSIONS = {
    ".py", ".sql", ".json", ".yaml", ".yml", ".toml",
    ".ini", ".cfg", ".conf", ".ps1", ".sh", ".env",
    ".txt", ".md", ".pem",
}

IGNORED_DIRECTORIES = {
    ".git", ".venv", ".venv-w5d1", "__pycache__",
    ".pytest_cache", "node_modules",
}

SEVERITY_ORDER = {
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1,
    "INFO": 0,
    "N/A": 0,
}


def sha256_file(file_path: Path) -> str:
    """Calculate a file's SHA-256 checksum."""
    digest = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def classify_column(column_name: str) -> str:
    """Classify columns by their potential identification risk."""
    name = str(column_name)

    if DIRECT_ID_PATTERN.search(name):
        return "Potential direct identifier"

    if INDIRECT_ID_PATTERN.search(name):
        return "Pseudonymous or indirect identifier"

    return "General business data"


def detect_sensitive_values(dataframe: pd.DataFrame) -> list:
    """Count possible sensitive-value patterns without exposing values."""
    findings = []

    for column in dataframe.columns:
        column_name = str(column)
        text_values = dataframe[column].dropna().astype(str)

        for pattern_name, pattern in VALUE_PATTERNS.items():
            # Phone-number patterns are checked only in relevant columns
            # to reduce false positives in ordinary business data.
            if pattern_name == "indian_mobile_like":
                if not re.search(
                    r"phone|mobile|contact", column_name, re.IGNORECASE
                ):
                    continue

            # Skip numeric columns unless their names suggest direct PII.
            if not (
                pd.api.types.is_object_dtype(dataframe[column])
                or pd.api.types.is_string_dtype(dataframe[column])
                or DIRECT_ID_PATTERN.search(column_name)
            ):
                continue

            count = int(
                text_values.str.contains(pattern, na=False).sum()
            )

            if count:
                findings.append({
                    "column": column_name,
                    "pattern": pattern_name,
                    "matched_rows": count,
                })

    return findings


def detect_secret_patterns(text: str) -> list:
    """Return secret rule names and line numbers, never matched values."""
    findings = []

    for line_number, line in enumerate(text.splitlines(), start=1):
        for rule_name, pattern in SECRET_PATTERNS.items():
            if pattern.search(line):
                findings.append({
                    "rule": rule_name,
                    "line": line_number,
                })

    return findings


def scan_repository_for_secrets(root: Path) -> list:
    """Scan eligible text and configuration files for exposed secrets."""
    findings = []

    for file_path in root.rglob("*"):
        if not file_path.is_file():
            continue

        relative_path = file_path.relative_to(root)
                # Never scan local environment files containing private credentials.
        if file_path.name == ".env" or file_path.name.startswith(".env."):
            continue

        if any(
            part in IGNORED_DIRECTORIES
            for part in relative_path.parts
        ):
            continue

        if "Week 12" in relative_path.parts and "outputs" in relative_path.parts:
            continue

        eligible_file = (
            file_path.suffix.lower() in SCANNED_EXTENSIONS
            or file_path.name == ".env"
        )

        if not eligible_file or file_path.stat().st_size > 1_000_000:
            continue

        try:
            content = file_path.read_text(
                encoding="utf-8",
                errors="ignore",
            )
        except OSError:
            continue

        for match in detect_secret_patterns(content):
            findings.append({
                "file": relative_path.as_posix(),
                "rule": match["rule"],
                "line": match["line"],
            })

    return findings


def build_record(
    check_id: str,
    category: str,
    check: str,
    status: str,
    severity: str,
    details: str,
    recommendation: str,
) -> dict:
    """Create a standardised audit result record."""
    return {
        "check_id": check_id,
        "category": category,
        "check": check,
        "status": status,
        "severity": severity,
        "details": details,
        "recommendation": recommendation,
    }


def run_audit() -> dict:
    """Run the local data and repository security checks."""
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    dataframe = pd.read_csv(DATASET_PATH)
    records = []

    dataset_hash = sha256_file(DATASET_PATH)

    records.append(build_record(
        "DATA-001",
        "Data integrity",
        "Dataset metadata and checksum",
        "PASS",
        "INFO",
        (
            f"Dataset loaded; rows={len(dataframe)}, "
            f"columns={len(dataframe.columns)}, "
            f"SHA-256={dataset_hash}"
        ),
        "Recalculate and compare the checksum when validating a dataset copy.",
    ))

    for column in dataframe.columns:
        classification = classify_column(str(column))

        if classification == "Potential direct identifier":
            status, severity = "REVIEW_REQUIRED", "HIGH"
            recommendation = (
                "Confirm the field is necessary; mask or remove it "
                "when it is not required."
            )
        elif classification == "Pseudonymous or indirect identifier":
            status, severity = "REVIEW_REQUIRED", "MEDIUM"
            recommendation = (
                "Restrict access and assess whether this identifier "
                "can be linked to an individual."
            )
        else:
            status, severity = "PASS", "LOW"
            recommendation = "Apply the platform's normal data controls."

        records.append(build_record(
            f"CLASS-{len(records):03d}",
            "Data classification",
            f"Column classification: {column}",
            status,
            severity,
            classification,
            recommendation,
        ))

    sensitive_findings = detect_sensitive_values(dataframe)

    if sensitive_findings:
        for item in sensitive_findings:
            records.append(build_record(
                f"PII-{len(records):03d}",
                "Sensitive data exposure",
                f"Pattern scan: {item['pattern']} in {item['column']}",
                "FAIL",
                "HIGH",
                (
                    f"Potential matches found in "
                    f"{item['matched_rows']} row(s); values not recorded."
                ),
                (
                    "Verify the matches securely. Mask, remove, or "
                    "restrict access to confirmed sensitive data."
                ),
            ))
    else:
        records.append(build_record(
            "PII-000",
            "Sensitive data exposure",
            "Email, Aadhaar-like and PAN-like pattern scan",
            "PASS",
            "LOW",
            "No matching patterns found in the scanned dataset fields.",
            "Repeat the scan when new data is introduced.",
        ))

    secret_findings = scan_repository_for_secrets(PROJECT_ROOT)

    if secret_findings:
        for item in secret_findings:
            records.append(build_record(
                f"SECRET-{len(records):03d}",
                "Credential security",
                f"Potential secret in {item['file']} at line {item['line']}",
                "FAIL",
                "HIGH",
                (
                    f"Potential {item['rule']} pattern detected; "
                    "the matching content was not recorded."
                ),
                (
                    "Verify the finding. Remove exposed credentials, "
                    "rotate affected secrets, and use a secure secret store."
                ),
            ))
    else:
        records.append(build_record(
            "SECRET-000",
            "Credential security",
            "Repository secret-pattern scan",
            "PASS",
            "LOW",
            "No supported secret patterns detected in eligible text files.",
            "Use secret scanning in version control and rotate any exposed keys.",
        ))

    records.append(build_record(
        "MANUAL-001",
        "Platform controls",
        "Access, encryption, MFA, logging, backup and retention review",
        "REVIEW_REQUIRED",
        "MEDIUM",
        (
            "These controls cannot be verified from a local CSV and "
            "repository scan."
        ),
        (
            "Inspect database permissions, least-privilege roles, "
            "encryption settings, MFA, audit logs, backup protection "
            "and retention policies with the platform administrator."
        ),
    ))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    report = pd.DataFrame(records)
    report_path = OUTPUT_DIR / "security_audit_report.csv"
    report.to_csv(report_path, index=False)

    counts = report["status"].value_counts().to_dict()

    summary = {
        "dataset": str(DATASET_PATH.relative_to(PROJECT_ROOT)),
        "rows_scanned": int(len(dataframe)),
        "columns_scanned": int(len(dataframe.columns)),
        "dataset_sha256": dataset_hash,
        "total_checks": int(len(report)),
        "status_counts": {
            "PASS": int(counts.get("PASS", 0)),
            "FAIL": int(counts.get("FAIL", 0)),
            "REVIEW_REQUIRED": int(counts.get("REVIEW_REQUIRED", 0)),
        },
        "report_file": report_path.name,
        "note": (
            "This is a local, pattern-based audit. A PASS does not prove "
            "the absence of all sensitive data or security vulnerabilities. "
            "Manual platform-control verification is required."
        ),
    }

    summary_path = OUTPUT_DIR / "security_audit_summary.json"
    summary_path.write_text(
        json.dumps(summary, indent=4),
        encoding="utf-8",
    )

    print("Security audit completed.")
    print(f"Rows scanned: {len(dataframe):,}")
    print(f"Columns scanned: {len(dataframe.columns)}")
    print(f"Total checks: {len(report)}")
    print(f"PASS: {summary['status_counts']['PASS']}")
    print(f"FAIL: {summary['status_counts']['FAIL']}")
    print(
        "REVIEW REQUIRED: "
        f"{summary['status_counts']['REVIEW_REQUIRED']}"
    )
    print(f"Report saved: {report_path}")
    print(f"Summary saved: {summary_path}")

    return summary


if __name__ == "__main__":
    run_audit()
