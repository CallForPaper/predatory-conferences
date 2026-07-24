#!/usr/bin/env python3
"""
archive_wayback.py

Sends a URL request to the Internet Archive (Wayback Machine) Save API
to save a page and return the archived URL.
"""

import sys
import time
import urllib.request
import urllib.parse
import json

def save_to_wayback(url):
    print(f"Requesting Wayback Machine archive for: {url}")
    # Save URL endpoint
    save_url = f"https://web.archive.org/save/{url}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    req = urllib.request.Request(save_url, headers=headers)
    
    # Try Save Page Now request
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            # Wayback machine returns redirect header or content location when saved successfully
            info = response.info()
            # Check content-location header
            location = info.get('Content-Location') or info.get('Location')
            if location:
                archive_url = f"https://web.archive.org{location}"
                print(f"✅ Archived successfully: {archive_url}")
                return archive_url
    except Exception as e:
        print(f"⚠️ Wayback Save request directly failed: {e}")

    # Fallback to checking availability if Save request fails / limits.
    # Check if a snapshot already exists using the Wayback Availability API
    print("Checking availability API for existing snapshots...")
    api_url = f"https://archive.org/wayback/available?url={urllib.parse.quote(url)}"
    try:
        with urllib.request.urlopen(api_url, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            snapshots = data.get("archived_snapshots", {})
            closest = snapshots.get("closest", {})
            if closest and closest.get("available"):
                archive_url = closest.get("url")
                print(f"✅ Found existing archive: {archive_url}")
                return archive_url
    except Exception as e:
        print(f"❌ Failed to check availability API: {e}")

    return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python archive_wayback.py <url>")
        sys.exit(1)
    
    target_url = sys.argv[1]
    archived = save_to_wayback(target_url)
    if archived:
        print(archived)
    else:
        print("")
        sys.exit(1)
