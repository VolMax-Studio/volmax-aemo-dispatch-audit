#!/usr/bin/env python3
"""Create Zenodo v2: add data_manifest.json and metrics JSONs to the existing record."""
import json
import os
import requests

ZENODO_API = "https://zenodo.org/api"
TOKEN = open(os.path.expanduser("~/.zenodo_token")).readline().strip()
HEADERS = {"Authorization": f"Bearer {TOKEN}"}
RECORD_ID = 21190094

# Files to add in v2
NEW_FILES = [
    ("data/data_manifest.json", "data_manifest.json"),
    ("data/processed/l1_integrity_report.json", "l1_integrity_report.json"),
    ("data/processed/verify_aemo_claims.json", "verify_aemo_claims.json"),
    ("data/processed/verify_aemo_fcas.json", "verify_aemo_fcas.json"),
]

def main():
    # Step 1: Create new version from existing record
    print(f"Creating new version of record {RECORD_ID}...")
    r = requests.post(
        f"{ZENODO_API}/deposit/depositions/{RECORD_ID}/actions/newversion",
        headers=HEADERS
    )
    r.raise_for_status()
    new_version_url = r.json()["links"]["latest_draft"]
    print(f"  Draft URL: {new_version_url}")

    # Step 2: Get the new draft details
    r = requests.get(new_version_url, headers=HEADERS)
    r.raise_for_status()
    draft = r.json()
    new_dep_id = draft["id"]
    bucket_url = draft["links"]["bucket"]
    print(f"  New deposit ID: {new_dep_id}")

    # Step 3: Upload additional files
    print(f"Uploading {len(NEW_FILES)} additional files...")
    for local_path, upload_name in NEW_FILES:
        if not os.path.exists(local_path):
            print(f"  SKIP (not found): {local_path}")
            continue
        with open(local_path, "rb") as fp:
            r = requests.put(
                f"{bucket_url}/{upload_name}",
                headers=HEADERS,
                data=fp,
            )
            r.raise_for_status()
        print(f"  Uploaded: {local_path} -> {upload_name}")

    # Step 4: Publish new version
    print("Publishing v2...")
    r = requests.post(
        f"{ZENODO_API}/deposit/depositions/{new_dep_id}/actions/publish",
        headers=HEADERS
    )
    r.raise_for_status()
    published = r.json()
    doi = published["doi"]
    doi_url = published["doi_url"]
    record_url = published["links"]["record_html"]
    print(f"\n{'='*60}")
    print(f"v2 PUBLISHED SUCCESSFULLY")
    print(f"  DOI:        {doi}")
    print(f"  DOI URL:    {doi_url}")
    print(f"  Record:     {record_url}")
    print(f"  Concept DOI still resolves to latest.")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
