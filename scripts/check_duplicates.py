#!/usr/bin/env python3
"""
Check for duplicate entries in a CSV column.
Usage: python check_duplicates.py <csv_file> <column_name>
"""

import sys
import csv
from collections import Counter


def check_duplicates(filepath: str, column: str) -> bool:
    values = []
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if column not in (reader.fieldnames or []):
            print(f"❌ Column '{column}' not found in {filepath}")
            return False
        for row in reader:
            val = row.get(column, "").strip().lower()
            if val:
                values.append(val)

    counts = Counter(values)
    duplicates = {v: c for v, c in counts.items() if c > 1}

    if duplicates:
        print(f"⚠️  Duplicate values found in '{column}' column of {filepath}:")
        for val, count in sorted(duplicates.items()):
            print(f"  '{val}' appears {count} times")
        return False
    else:
        print(f"✅ No duplicates found in '{column}' column of {filepath}")
        return True


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python check_duplicates.py <csv_file> <column_name>")
        sys.exit(1)

    success = check_duplicates(sys.argv[1], sys.argv[2])
    sys.exit(0 if success else 1)