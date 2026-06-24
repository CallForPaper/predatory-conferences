#!/usr/bin/env python3
"""
Validate dataset CSV files for schema compliance and data quality.
Usage: python validate.py <csv_file> <schema_type>
"""

import sys
import csv
import re
from pathlib import Path

SCHEMAS = {
    "organizers": {
        "required_columns": ["name", "domain", "aliases", "status", "evidence_url", "source", "added_date", "notes"],
        "valid_statuses": {"confirmed", "suspected", "disputed"},
    },
    "conferences": {
        "required_columns": ["name", "organizer_domain", "broad_field", "status", "evidence_url", "source", "added_date", "notes"],
        "valid_statuses": {"confirmed", "suspected", "disputed"},
    },
}

DOMAIN_PATTERN = re.compile(r'^[a-z0-9][a-z0-9\-\.]+\.[a-z]{2,}$')
DATE_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2}$')


def validate_csv(filepath: str, schema_type: str) -> bool:
    schema = SCHEMAS.get(schema_type)
    if not schema:
        print(f"❌ Unknown schema type: {schema_type}")
        return False

    path = Path(filepath)
    if not path.exists():
        print(f"❌ File not found: {filepath}")
        return False

    errors = []
    warnings = []

    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        actual_columns = reader.fieldnames or []

        # Check required columns
        for col in schema["required_columns"]:
            if col not in actual_columns:
                errors.append(f"Missing required column: '{col}'")

        if errors:
            for e in errors:
                print(f"❌ {e}")
            return False

        for i, row in enumerate(reader, start=2):  # start=2 for header row
            row_id = f"Row {i}"

            # Check status
            status = row.get("status", "").strip()
            if status not in schema["valid_statuses"]:
                errors.append(f"{row_id}: Invalid status '{status}' (must be one of {schema['valid_statuses']})")

            # Check date format
            date = row.get("added_date", "").strip()
            if date and not DATE_PATTERN.match(date):
                errors.append(f"{row_id}: Invalid date format '{date}' (must be YYYY-MM-DD)")

            # Check domain format
            domain_field = "domain" if schema_type == "organizers" else "organizer_domain"
            domain = row.get(domain_field, "").strip()
            if domain and not DOMAIN_PATTERN.match(domain):
                warnings.append(f"{row_id}: Domain '{domain}' looks unusual")

            # Warn if confirmed but no evidence URL
            if status == "confirmed" and not row.get("evidence_url", "").strip():
                warnings.append(f"{row_id}: Status is 'confirmed' but no evidence_url provided")

            # Check name is not empty
            name = row.get("name", "").strip()
            if not name:
                errors.append(f"{row_id}: Name is empty")

    if errors:
        print(f"\n❌ VALIDATION FAILED: {filepath}")
        for e in errors:
            print(f"  ERROR: {e}")
    else:
        print(f"\n✅ VALIDATION PASSED: {filepath}")

    if warnings:
        print(f"\n⚠️  Warnings ({len(warnings)}):")
        for w in warnings:
            print(f"  WARN: {w}")

    return len(errors) == 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python validate.py <csv_file> <schema_type>")
        sys.exit(1)

    success = validate_csv(sys.argv[1], sys.argv[2])
    sys.exit(0 if success else 1)