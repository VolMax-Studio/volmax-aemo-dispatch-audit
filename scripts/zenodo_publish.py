#!/usr/bin/env python3
"""Publish the AEMO BESS audit to Zenodo and retrieve the DOI."""
import json
import os
import sys
import requests

ZENODO_API = "https://zenodo.org/api"
TOKEN = open(os.path.expanduser("~/.zenodo_token")).readline().strip()
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# Files to upload (source code, reports, plots, metadata)
UPLOAD_FILES = [
    "README.md",
    "reproduce.py",
    "requirements.txt",
    "download_aemo_data.py",
    "compile_l1_integrity.py",
    "compile_fcas_frequency.py",
    "verify_aemo_claims.py",
    "verify_aemo_fcas.py",
    "l1_integrity_report.md",
    "l2_conformance_report.md",
    "l2_conformance_report.sha256",
    "l3_fcas_report.md",
    "l3_fcas_report.sha256",
    "results/plot1_conformance_exceedance.png",
    "results/plot2_efc_vs_standby.png",
    "results/plot3_fcas_event_august19.png",
    ".zenodo.json",
    "CITATION.cff",
    "LICENSE",
]

def main():
    # Load metadata from .zenodo.json
    with open(".zenodo.json") as f:
        zmeta = json.load(f)

    # Step 1: Create empty deposit
    print("Creating Zenodo deposit...")
    r = requests.post(f"{ZENODO_API}/deposit/depositions",
                      headers={**HEADERS, "Content-Type": "application/json"},
                      json={})
    r.raise_for_status()
    deposition = r.json()
    dep_id = deposition["id"]
    bucket_url = deposition["links"]["bucket"]
    print(f"  Deposit created: ID={dep_id}")

    # Step 2: Upload files
    print(f"Uploading {len(UPLOAD_FILES)} files...")
    for filepath in UPLOAD_FILES:
        if not os.path.exists(filepath):
            print(f"  SKIP (not found): {filepath}")
            continue
        filename = os.path.basename(filepath)
        # Use bucket API for large file support
        with open(filepath, "rb") as fp:
            r = requests.put(
                f"{bucket_url}/{filename}",
                headers=HEADERS,
                data=fp,
            )
            r.raise_for_status()
        print(f"  Uploaded: {filepath} -> {filename}")

    # Step 3: Set metadata
    print("Setting metadata...")
    metadata = {
        "metadata": {
            "title": zmeta["title"],
            "upload_type": "dataset",
            "description": zmeta["description"],
            "creators": zmeta["creators"],
            "access_right": zmeta["access_right"],
            "license": zmeta["license"],
            "keywords": zmeta["keywords"],
            "notes": zmeta["notes"],
        }
    }
    r = requests.put(f"{ZENODO_API}/deposit/depositions/{dep_id}",
                     headers={**HEADERS, "Content-Type": "application/json"},
                     json=metadata)
    r.raise_for_status()
    print("  Metadata set.")

    # Step 4: Publish
    print("Publishing deposit...")
    r = requests.post(f"{ZENODO_API}/deposit/depositions/{dep_id}/actions/publish",
                      headers=HEADERS)
    r.raise_for_status()
    published = r.json()
    doi = published["doi"]
    doi_url = published["doi_url"]
    record_url = published["links"]["record_html"]
    print(f"\n{'='*60}")
    print(f"PUBLISHED SUCCESSFULLY")
    print(f"  DOI:        {doi}")
    print(f"  DOI URL:    {doi_url}")
    print(f"  Record:     {record_url}")
    print(f"{'='*60}")

    # Write DOI to a local file for downstream use
    with open("zenodo_doi.txt", "w") as f:
        f.write(f"{doi}\n{doi_url}\n{record_url}\n")
    print(f"DOI saved to zenodo_doi.txt")

if __name__ == "__main__":
    main()
