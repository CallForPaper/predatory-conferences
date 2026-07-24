#!/usr/bin/env python3
"""
validate_entities.py

Validates YAML data files in organizers/ and conferences/ against schema/entity.schema.json,
performing cross-reference verification and format checks.
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime

# Optional dependency check for jsonschema and pyyaml
try:
    import jsonschema
    import yaml
except ImportError:
    print("Error: Required dependencies (jsonschema, pyyaml) not installed.")
    print("Please install them with: pip install jsonschema pyyaml")
    sys.exit(1)

SCHEMA_PATH = Path("schema/entity.schema.json")
DATE_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2}$')

def validate_date(date_str, field_name, file_path):
    if not date_str:
        return
    if not DATE_PATTERN.match(date_str):
        print(f"❌ Error in {file_path}: Field '{field_name}' date format '{date_str}' is invalid. Must be YYYY-MM-DD.")
        sys.exit(1)
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        if dt > datetime.now():
            print(f"❌ Error in {file_path}: Field '{field_name}' date '{date_str}' is in the future.")
            sys.exit(1)
    except ValueError:
        print(f"❌ Error in {file_path}: Field '{field_name}' contains an invalid date value '{date_str}'.")
        sys.exit(1)

def validate_entity_file(file_path, schema, organizers_slugs):
    # Load YAML file
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Error in {file_path}: Failed to parse YAML file. Reason: {e}")
        sys.exit(1)

    # Validate against JSON Schema
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        print(f"❌ Schema validation failed in {file_path}:")
        print(f"  Field: {' -> '.join(str(p) for p in e.absolute_path)}")
        print(f"  Error: {e.message}")
        sys.exit(1)

    # File path convention verification
    slug = data.get("slug")
    file_slug = file_path.stem
    if slug != file_slug:
        print(f"❌ Error in {file_path}: File basename '{file_slug}' must match entity slug '{slug}'.")
        sys.exit(1)

    entity_type = data.get("type")

    # Cross-reference check: evidence_refs inside red_flags must map to items in evidence
    evidence_ids = set()
    for ev in data.get("evidence", []):
        ev_id = ev.get("id")
        if ev_id in evidence_ids:
            print(f"❌ Error in {file_path}: Duplicate evidence ID '{ev_id}' found.")
            sys.exit(1)
        evidence_ids.add(ev_id)
        
        # Verify snapshot_file path actually exists if provided
        snapshot = ev.get("snapshot_file")
        if snapshot:
            snapshot_path = Path(snapshot)
            # Create a mock or placeholder checking if it contains PLACEHOLDER/dummy files
            # For checking, standard files should exist in the repository
            if not snapshot_path.exists():
                print(f"⚠️ Warning in {file_path}: snapshot_file path '{snapshot}' does not exist locally.")

    red_flag_ids = set()
    for rf in data.get("red_flags", []):
        rf_id = rf.get("id")
        if rf_id in red_flag_ids:
            print(f"❌ Error in {file_path}: Duplicate red flag ID '{rf_id}' found.")
            sys.exit(1)
        red_flag_ids.add(rf_id)

        for ref in rf.get("evidence_refs", []):
            if ref not in evidence_ids:
                print(f"❌ Error in {file_path}: Red flag '{rf_id}' references non-existent evidence ID '{ref}'.")
                sys.exit(1)

    dispute_ids = set()
    for d in data.get("disputes", []):
        d_id = d.get("id")
        if d_id in dispute_ids:
            print(f"❌ Error in {file_path}: Duplicate dispute ID '{d_id}' found.")
            sys.exit(1)
        dispute_ids.add(d_id)

    # Date validations
    validate_date(data.get("first_flagged"), "first_flagged", file_path)
    validate_date(data.get("last_updated"), "last_updated", file_path)
    validate_date(data.get("last_reviewed"), "last_reviewed", file_path)

    for rf in data.get("red_flags", []):
        validate_date(rf.get("first_observed"), "red_flags[].first_observed", file_path)
        validate_date(rf.get("last_confirmed"), "red_flags[].last_confirmed", file_path)

    for ev in data.get("evidence", []):
        validate_date(ev.get("date"), "evidence[].date", file_path)

    for d in data.get("disputes", []):
        validate_date(d.get("opened_date"), "disputes[].opened_date", file_path)
        validate_date(d.get("resolution_date"), "disputes[].resolution_date", file_path)

    # Conference specific checks
    if entity_type == "conference":
        org_slug = data.get("organizer_slug")
        if org_slug not in organizers_slugs:
            print(f"❌ Error in {file_path}: organizer_slug '{org_slug}' does not correspond to a valid file in organizers/")
            sys.exit(1)

    return slug, entity_type

def main():
    if not SCHEMA_PATH.exists():
        print(f"❌ Schema file not found at: {SCHEMA_PATH}")
        sys.exit(1)

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)

    # Scan organizers first to establish slug mappings
    organizers_slugs = set()
    organizer_files = list(Path("organizers").glob("*.yaml")) + list(Path("organizers").glob("*.yml"))
    
    print(f"Scanning {len(organizer_files)} organizers...")
    for file_path in organizer_files:
        slug, etype = validate_entity_file(file_path, schema, organizers_slugs)
        if etype != "organizer":
            print(f"❌ Error in {file_path}: Entity type must be 'organizer' under organizers/ folder.")
            sys.exit(1)
        if slug in organizers_slugs:
            print(f"❌ Error: Duplicate organizer slug '{slug}' found at {file_path}.")
            sys.exit(1)
        organizers_slugs.add(slug)

    # Scan conferences
    conference_files = list(Path("conferences").rglob("*.yaml")) + list(Path("conferences").rglob("*.yml"))
    conference_slugs = set()
    
    print(f"Scanning {len(conference_files)} conferences...")
    for file_path in conference_files:
        # Ignore template if any
        slug, etype = validate_entity_file(file_path, schema, organizers_slugs)
        if etype != "conference":
            print(f"❌ Error in {file_path}: Entity type must be 'conference' under conferences/ folder.")
            sys.exit(1)
        if slug in conference_slugs:
            print(f"❌ Error: Duplicate conference slug '{slug}' found at {file_path}.")
            sys.exit(1)
        conference_slugs.add(slug)

    print("✅ All entity validation checks passed successfully.")

if __name__ == "__main__":
    main()
