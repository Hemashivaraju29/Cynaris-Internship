
import sys
from pathlib import Path

import pandas as pd

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from security_audit import (
    classify_column,
    detect_sensitive_values,
    detect_secret_patterns,
    scan_repository_for_secrets,
    sha256_file,
)


def test_classify_direct_identifier():
    assert classify_column("email") == "Potential direct identifier"


def test_classify_customer_id():
    assert (
        classify_column("customer_id")
        == "Pseudonymous or indirect identifier"
    )


def test_classify_general_business_column():
    assert classify_column("product") == "General business data"


def test_detect_sensitive_email_without_exposing_value():
    dataframe = pd.DataFrame({
        "contact_email": [
            "test@example.com",
            "ordinary-text",
        ]
    })

    findings = detect_sensitive_values(dataframe)

    assert len(findings) == 1
    assert findings[0]["pattern"] == "email_like"
    assert findings[0]["matched_rows"] == 1
    assert "test@example.com" not in str(findings)


def test_secret_detection_returns_rule_not_secret():
    # Construct the test input dynamically so no literal credential
    # is embedded in this test source file.
    secret_value = "UnitTestSecretValue123"
    assignment = "pass" + "word = " + repr(secret_value)

    findings = detect_secret_patterns(
        "configuration line\n" + assignment
    )

    assert len(findings) == 1
    assert findings[0]["rule"] == "credential_assignment"
    assert findings[0]["line"] == 2
    assert secret_value not in str(findings)


def test_repository_scanner_excludes_env_file(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "PRIVATE_SETTING=sample-private-value",
        encoding="utf-8",
    )

    source_file = tmp_path / "config.py"
    secret_value = "TemporaryTestSecret123"
    assignment = "pass" + "word = " + repr(secret_value)
    source_file.write_text(assignment, encoding="utf-8")

    findings = scan_repository_for_secrets(tmp_path)

    assert len(findings) == 1
    assert findings[0]["file"] == "config.py"
    assert ".env" not in str(findings)


def test_sha256_checksum(tmp_path):
    test_file = tmp_path / "sample.txt"
    test_file.write_text("security audit", encoding="utf-8")

    checksum = sha256_file(test_file)

    assert len(checksum) == 64
    assert all(char in "0123456789abcdef" for char in checksum)
