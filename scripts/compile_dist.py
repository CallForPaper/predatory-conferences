#!/usr/bin/env python3
"""
compile_dist.py

Walks organizers/ and conferences/ yaml files and compiles them into flat lists.
Outputs to dist/organizers.json and dist/conferences.json.
Includes compiled_at timestamp and entity count summary.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Please run: pip install pyyaml")
    sys.exit(1)

ORGANIZERS_DIR = Path("organizers")
CONFERENCES_DIR = Path("conferences")
DIST_DIR = Path("dist")

def load_yaml_files(directory):
    entities = []
    # Support recursive traversal for conferences, or flat glob for organizers
    files = list(directory.rglob("*.yaml")) + list(directory.rglob("*.yml"))
    for file_path in sorted(files):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if data:
                    entities.append(data)
        except Exception as e:
            print(f"❌ Error loading {file_path}: {e}")
            sys.exit(1)
    return entities

def main():
    DIST_DIR.mkdir(exist_ok=True)

    print("Compiling organizers...")
    organizers = load_yaml_files(ORGANIZERS_DIR)

    print("Compiling conferences...")
    conferences = load_yaml_files(CONFERENCES_DIR)

    # Wrap inside compilation envelope
    compiled_at = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    org_output = {
        "compiled_at": compiled_at,
        "count": len(organizers),
        "data": organizers
    }

    conf_output = {
        "compiled_at": compiled_at,
        "count": len(conferences),
        "data": conferences
    }

    org_dist_file = DIST_DIR / "organizers.json"
    conf_dist_file = DIST_DIR / "conferences.json"

    with open(org_dist_file, "w", encoding="utf-8") as f:
        json.dump(org_output, f, indent=2, sort_keys=False)

    with open(conf_dist_file, "w", encoding="utf-8") as f:
        json.dump(conf_output, f, indent=2, sort_keys=False)

    print(f"✅ Compilation finished successfully.")
    print(f"  Organizers compiled: {len(organizers)} -> {org_dist_file}")
    print(f"  Conferences compiled: {len(conferences)} -> {conf_dist_file}")

if __name__ == "__main__":
    main()
