#!/usr/bin/env python3
"""
Generate dataset statistics summary.
"""

import csv
from collections import Counter
from pathlib import Path


def count_by_status(filepath):
    counts = Counter()
    try:
        with open(filepath, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                counts[row.get("status", "unknown").strip()] += 1
    except FileNotFoundError:
        pass
    return counts


def main():
    org_stats = count_by_status("data/organizers.csv")
    conf_stats = count_by_status("data/conferences.csv")

    total_orgs = sum(org_stats.values())
    total_confs = sum(conf_stats.values())

    print("\n📊 Dataset Statistics")
    print("=" * 40)
    print(f"\nOrganizers ({total_orgs} total):")
    for status, count in sorted(org_stats.items()):
        print(f"  {status}: {count}")

    print(f"\nConferences ({total_confs} total):")
    for status, count in sorted(conf_stats.items()):
        print(f"  {status}: {count}")

    print(f"\nTotal entries: {total_orgs + total_confs}")
    print("=" * 40)


if __name__ == "__main__":
    main()