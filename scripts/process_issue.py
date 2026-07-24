#!/usr/bin/env python3
"""
process_issue.py

Parses a GitHub Issue payload, checks for duplicates, retrieves a Wayback archive url,
and generates the appropriate YAML entity structure.
"""

import os
import sys
import json
import re
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required.")
    sys.exit(1)

# Helper to import wayback function
from archive_wayback import save_to_wayback

def clean_slug(name):
    s = name.lower()
    s = re.sub(r'^https?://(?:www\.)?', '', s)
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-')

def check_domain_duplicate(domain):
    # Scan organizers yaml files
    organizer_files = list(Path("organizers").glob("*.yaml")) + list(Path("organizers").glob("*.yml"))
    for file_path in organizer_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if data and domain.lower() in [d.lower() for d in data.get("domains", [])]:
                    return data.get("slug"), "organizer"
        except Exception:
            pass
    return None, None

def check_conference_duplicate(name):
    # Scan conferences yaml files
    conference_files = list(Path("conferences").rglob("*.yaml")) + list(Path("conferences").rglob("*.yml"))
    for file_path in conference_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if data and name.lower() == data.get("name", "").lower():
                    return data.get("slug"), "conference"
        except Exception:
            pass
    return None, None

def parse_markdown_issue(body):
    # Standard Markdown block parsing for fields in issue template
    fields = {}
    current_key = None
    lines = body.split("\n")
    for line in lines:
        if line.startswith("### "):
            current_key = line.replace("### ", "").strip().lower().replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_")
            fields[current_key] = []
        elif current_key:
            fields[current_key].append(line)
            
    for k in fields:
        fields[k] = "\n".join(fields[k]).strip()
        
    return fields

def main():
    issue_body_path = os.getenv("ISSUE_BODY_FILE")
    issue_labels = os.getenv("ISSUE_LABELS", "")
    
    if not issue_body_path or not Path(issue_body_path).exists():
        print("❌ Issue payload file not found.")
        sys.exit(1)

    with open(issue_body_path, "r", encoding="utf-8") as f:
        body = f.read()

    parsed = parse_markdown_issue(body)
    
    # Identify type based on labels
    is_organizer = "organizer-report" in issue_labels
    is_conference = "conference-report" in issue_labels

    if not is_organizer and not is_conference:
        print("❌ Issue lacks matching labels ('organizer-report' or 'conference-report').")
        sys.exit(1)

    # 1. Parse common information
    name = parsed.get("organizer_name", parsed.get("conference_name", "")).strip()
    evidence_url = parsed.get("source_evidence_url", parsed.get("source_url", "")).strip()
    red_flag_category = parsed.get("primary_red_flag_category", "").strip()
    description = parsed.get("evidence_description", "").strip()
    
    if not name:
        print("❌ Error: Could not parse name field from issue template.")
        sys.exit(1)

    # 2. Duplicate Check
    if is_organizer:
        domains_raw = parsed.get("primary_domain_s", "").strip()
        domains = [d.strip() for d in domains_raw.split("\n") if d.strip()]
        
        for d in domains:
            dup_slug, dup_type = check_domain_duplicate(d)
            if dup_slug:
                print(f"DUPLICATE_FOUND: organizer {dup_slug} (Domain matches: {d})")
                sys.exit(0)
    else:
        # Check conference duplicate
        dup_slug, dup_type = check_conference_duplicate(name)
        if dup_slug:
            print(f"DUPLICATE_FOUND: conference {dup_slug} (Name matches)")
            sys.exit(0)

    # 3. Wayback Machine Archiving
    archive_url = None
    if evidence_url and evidence_url.startswith("http"):
        archive_url = save_to_wayback(evidence_url)

    # 4. Generate YAML Entity Schema
    today = datetime.now().strftime('%Y-%m-%d')
    slug = clean_slug(name)
    
    evidence_item = {
        "id": "ev-1",
        "date": today,
        "type": "initial_detection",
        "observed_by": "community-contributor"
    }
    if evidence_url:
        evidence_item["source_url"] = evidence_url
    if archive_url:
        evidence_item["archive_org_url"] = archive_url

    red_flag_item = {
        "id": "rf-1",
        "type": red_flag_category if red_flag_category else "other",
        "description": description if description else "No detailed description recorded.",
        "first_observed": today,
        "status": "active",
        "evidence_refs": ["ev-1"]
    }

    if is_organizer:
        domains_raw = parsed.get("primary_domain_s", "").strip()
        domains = [d.strip() for d in domains_raw.split("\n") if d.strip()]
        network = parsed.get("parent_network___affiliation_optional", "").strip()
        
        entity = {
            "type": "organizer",
            "slug": slug,
            "status": "active_flag",
            "criteria_version": "v1.0",
            "first_flagged": today,
            "last_updated": today,
            "last_reviewed": today,
            "name": name,
            "domains": domains,
            "red_flags": [red_flag_item],
            "evidence": [evidence_item],
            "disputes": []
        }
        if network:
            entity["network"] = network

        # Save organizer file
        out_file = Path("organizers") / f"{slug}.yaml"
        with open(out_file, "w", encoding="utf-8") as f:
            yaml.dump(entity, f, default_flow_style=False, sort_keys=False)
        print(f"SUCCESS: Created organizer entity {slug}")
        
    elif is_conference:
        org_slug = parsed.get("parent_organizer_name___slug_if_known", "unknown-organizer").strip()
        org_slug = clean_slug(org_slug) if org_slug else "unknown-organizer"
        
        event_dates_raw = parsed.get("event_dates", "").strip()
        event_dates = [d.strip() for d in event_dates_raw.split("\n") if d.strip()]
        venue = parsed.get("event_venue", "Unknown Venue").strip()

        entity = {
            "type": "conference",
            "slug": slug,
            "status": "active_flag",
            "criteria_version": "v1.0",
            "first_flagged": today,
            "last_updated": today,
            "last_reviewed": today,
            "name": name,
            "organizer_slug": org_slug,
            "event_dates": event_dates if event_dates else [today],
            "venue": venue,
            "source_url": evidence_url if evidence_url else "https://example.com/source",
            "red_flags": [red_flag_item],
            "evidence": [evidence_item],
            "disputes": []
        }

        # Save conference file
        conf_dir = Path("conferences") / org_slug
        conf_dir.mkdir(exist_ok=True)
        out_file = conf_dir / f"{slug}.yaml"
        with open(out_file, "w", encoding="utf-8") as f:
            yaml.dump(entity, f, default_flow_style=False, sort_keys=False)
        print(f"SUCCESS: Created conference entity {slug} under {org_slug}")

if __name__ == "__main__":
    main()
