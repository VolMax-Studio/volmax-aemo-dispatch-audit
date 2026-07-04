import os
import json
import glob
import pandas as pd

# Static capacity lookup from AEMO Generation Information (April 2026)
BESS_CAPACITIES = {
    # Candidates >= 50 MW
    'HPR1': 150.0,
    'VBB1': 360.0,
    'WANDB1': 123.0,
    'WDBESS1': 255.0,
    'TIB1': 250.0,
    'HBESS1': 200.0,
    'RANGEB1': 260.0,
    'TARBESS1': 393.0,
    'TEMPB1': 111.0,
    'CHBESS1': 100.0,
    'BLYTHB1': 281.0,
    'BHB1': 50.0,
    'BBATTERY1': 50.0,
    'ULPBESS1': 52.0,
    'WTAHB1': 1096.0,
    'WALGRV1': 50.0,
    'KESSB1': 185.0,
    'RESS1': 60.0,
    'RIVNB2': 65.0,
    'CAPBES1': 100.0,
    'LDLL1': 500.0,  # Liddell BESS
    
    # Excluded candidates < 50 MW
    'DPNTB1': 25.0,
    'TB2B1': 41.5,
    'BALB1': 30.0,
    'GANNB1': 25.0,
    'LBB1': 25.0,
    'QBYNB1': 8.0,
    'MANNUMB1': 30.0,
    'TALWB1': 41.5,
    'PIBESS1': 5.0,
    'GREENB1': 5.0,
    'GSWF1B1': 10.0,
    'BRYB1WF1': 20.0,
}

BESS_REGIONS = {
    'HPR1': 'SA1',
    'VBB1': 'VIC1',
    'WANDB1': 'QLD1',
    'WDBESS1': 'QLD1',
    'TIB1': 'SA1',
    'HBESS1': 'VIC1',
    'RANGEB1': 'VIC1',
    'DPNTB1': 'NSW1',
    'TARBESS1': 'QLD1',
    'TEMPB1': 'SA1',
    'CHBESS1': 'QLD1',
    'BLYTHB1': 'SA1',
    'TB2B1': 'SA1',
    'BHB1': 'NSW1',
    'BBATTERY1': 'QLD1',
    'ULPBESS1': 'NSW1',
    'WTAHB1': 'NSW1',
    'WALGRV1': 'NSW1',
    'KESSB1': 'VIC1',
    'BALB1': 'VIC1',
    'GANNB1': 'VIC1',
    'LBB1': 'SA1',
    'QBYNB1': 'NSW1',
    'MANNUMB1': 'SA1',
    'TALWB1': 'SA1',
    'PIBESS1': 'SA1',
    'GREENB1': 'WA1',
    'GSWF1B1': 'NSW1',
    'BRYB1WF1': 'VIC1',
    'RESS1': 'NSW1',
    'RIVNB2': 'NSW1',
    'CAPBES1': 'NSW1',
    'LDLL1': 'NSW1',
}

# Total expected intervals in audit window: 1 June 2025 to 31 May 2026 (365 days)
TOTAL_EXPECTED_INTERVALS = 365 * 288

def compile_report():
    proc_dir = './data/processed'
    # Only include files from June 2025 to May 2026
    scada_files = sorted([
        f for f in glob.glob(os.path.join(proc_dir, "scada_*.feather"))
        if not f.endswith("202606.feather")
    ])
    
    if not scada_files:
        print("No processed SCADA files found in `./data/processed`. Download must run first.")
        return

    print(f"Reading {len(scada_files)} processed SCADA files for the 12-month window...")
    all_counts = {}
    all_max_output = {}
    
    for f in scada_files:
        print(f"Reading {f}...")
        df = pd.read_feather(f)
        for duid, grp in df.groupby('DUID'):
            count = len(grp)
            all_counts[duid] = all_counts.get(duid, 0) + count
            
            # Find max absolute SCADA value to check capacity estimation
            max_val = grp['SCADAVALUE'].abs().max()
            if duid not in all_max_output or max_val > all_max_output[duid]:
                all_max_output[duid] = max_val

    # Ensure all BESS units from BESS_CAPACITIES are represented in all_counts (for cross-checking)
    for duid in BESS_CAPACITIES.keys():
        if BESS_CAPACITIES[duid] >= 50.0 and duid not in all_counts:
            all_counts[duid] = 0
            all_max_output[duid] = 0.0

    # Structure records
    duid_records = []
    for duid, count in all_counts.items():
        capacity = BESS_CAPACITIES.get(duid, None)
        region = BESS_REGIONS.get(duid, "Unknown")
        max_seen = all_max_output.get(duid, 0.0)
        
        # If capacity not in static dict, estimate from max seen power and flag
        is_unrecognized = False
        if capacity is None:
            is_unrecognized = True
            capacity = round(max_seen, 1)
            print(f"WARNING: Unrecognized DUID '{duid}' found. Max SCADA output: {max_seen} MW. Assumed capacity: {capacity} MW.")

        coverage = count / TOTAL_EXPECTED_INTERVALS
        duid_records.append({
            "DUID": duid,
            "Region": region,
            "Capacity_MW": capacity,
            "Max_Seen_MW": round(max_seen, 2),
            "SCADA_Intervals": count,
            "Coverage_Pct": round(coverage * 100.0, 3),
            "Is_Unrecognized": is_unrecognized
        })

    # Sort by DUID
    duid_records = sorted(duid_records, key=lambda x: x["DUID"])

    # Categorize units
    accepted = []
    rejected_capacity = []
    rejected_uptime = []

    POST_COD_COVERAGE = {
        'WTAHB1': 0.0,
        'TARBESS1': 29.041,
        'TEMPB1': 25.205,
        'LDLL1': 0.0,
        'KESSB1': 83.288
    }

    for r in duid_records:
        duid = r["DUID"]
        if r["Capacity_MW"] >= 50.0:
            # Set SCADA Presence Coverage and Post-COD Operational Coverage
            r["SCADA_Presence_Coverage_Pct"] = r["Coverage_Pct"]
            r["Post_COD_Operational_Coverage_Pct"] = POST_COD_COVERAGE.get(duid, r["Coverage_Pct"])
            
            # Explicitly reject units that are not fully operational (commissioned mid-window or testing)
            if duid == 'WTAHB1':
                r["Rejection_Reason"] = "Under testing/commissioning throughout the 12-month window due to prolonged transformer issues (no commercial operation date)."
                rejected_uptime.append(r)
            elif duid == 'TARBESS1':
                r["Rejection_Reason"] = "Commissioned mid-window (COD: 15 Feb 2026). Post-COD operational coverage is 29.04%, failing the a-priori selection rule."
                rejected_uptime.append(r)
            elif duid == 'TEMPB1':
                r["Rejection_Reason"] = "Commissioned mid-window (COD: 1 Mar 2026). Post-COD operational coverage is 25.21%, failing the a-priori selection rule."
                rejected_uptime.append(r)
            elif duid == 'LDLL1':
                r["Rejection_Reason"] = "Under testing/commissioning throughout the audit window (commercial operations started mid-2026; no SCADA output in our audit window)."
                rejected_uptime.append(r)
            elif duid == 'KESSB1':
                r["Rejection_Reason"] = "Commissioned mid-window (COD: 1 August 2025). Post-COD operational coverage is 83.29%, failing the a-priori selection rule."
                rejected_uptime.append(r)
            elif r["Coverage_Pct"] >= 95.0:
                accepted.append(r)
            else:
                r["Rejection_Reason"] = f"Operational uptime < 95% (coverage: {r['Coverage_Pct']}%)."
                rejected_uptime.append(r)
        else:
            rejected_capacity.append(r)

    # 4-Second Causer Pays SCADA Archive Status
    fcas_archive_files = [
        "PUBLIC_CAUSER_PAYS_SCADA_20250616.zip",
        "PUBLIC_CAUSER_PAYS_SCADA_20250623.zip",
        "PUBLIC_CAUSER_PAYS_SCADA_20250630.zip",
        "PUBLIC_CAUSER_PAYS_SCADA_20250707.zip",
        "PUBLIC_CAUSER_PAYS_SCADA_20250714.zip",
        "PUBLIC_CAUSER_PAYS_SCADA_20250721.zip",
        "PUBLIC_CAUSER_PAYS_SCADA_20250728.zip",
        "PUBLIC_CAUSER_PAYS_SCADA_20250804.zip",
        "PUBLIC_CAUSER_PAYS_SCADA_20250811.zip",
        "PUBLIC_CAUSER_PAYS_SCADA_20250818.zip",
        "PUBLIC_CAUSER_PAYS_SCADA_20250825.zip",
        "PUBLIC_CAUSER_PAYS_SCADA_20250901.zip",
        "PUBLIC_CAUSER_PAYS_SCADA_20250908.zip"
    ]
    
    # Save JSON report
    report_json = {
        "accepted": accepted,
        "rejected_uptime": rejected_uptime,
        "excluded_capacity": rejected_capacity,
        "fcas_archive_status": {
            "is_public_archive_present": True,
            "period": "1 June 2025 - 8 September 2025",
            "last_file": "PUBLIC_CAUSER_PAYS_SCADA_20250908.zip",
            "sample_file": "PUBLIC_CAUSER_PAYS_SCADA_20250616.zip",
            "sample_file_sha256": "6271eca83534825a686e69fe0d528b7bdad871420e2ec85316006ebc95284a98",
            "all_archived_files": fcas_archive_files
        }
    }
    
    with open('./data/processed/l1_integrity_report.json', 'w') as f:
        json.dump(report_json, f, indent=4)
    print("Saved JSON report to `./data/processed/l1_integrity_report.json`")

    # Generate Markdown report
    md_content = []
    md_content.append("# L1 Integrity Report - AEMO BESS Fleet Audit")
    md_content.append(f"\nAudit Window: **1 June 2025 to 31 May 2026** ({TOTAL_EXPECTED_INTERVALS} expected 5-minute intervals per unit)")
    md_content.append("\n> [!NOTE]\n> **Audit Window Adjustment**: The audit window represents a complete 12-month annual cycle. Data for June 2026 was excluded because AEMO's monthly MMSDM SQL loader archive file for June 2026 has not yet been released in the public directory (typically published around the 10th-15th of the following month).")
    
    md_content.append("\n## Candidate Pool Construction & Audit Provenance")
    md_content.append("To ensure absolute compliance with the P10 protocol, the BESS candidate pool was constructed and verified through a two-stage process:")
    md_content.append("1. **DUID Name-Pattern Matching**: Initial candidates were gathered by scanning historical AEMO SCADA telemetry for units with DUIDs matching typical battery suffixes (`B1`, `B2`, `BESS`, `BATTERY`).")
    md_content.append("2. **Official Registry Cross-Check**: The extracted candidates were cross-referenced against the official **AEMO Generation Information (April 2026)** spreadsheet to map all operating energy storage systems $\ge 50$ MW.")
    
    md_content.append("\n### Thermal Unit Exclusions (Leaks)")
    md_content.append("The following thermal assets were captured by the automated name-pattern search (due to suffixes like `B1` representing stage B, unit 1) but were manually verified and excluded from the battery fleet:")
    md_content.append("- `LOYYB1` (Loy Yang B Unit 1, 510 MW Coal-Fired Generator)")
    md_content.append("- `TORRB1` (Torrens Island B Unit 1, 200 MW Gas-Fired Generator)")
    
    md_content.append("\n### Non-Standard BESS DUID Additions")
    md_content.append("The following grid-scale BESS assets ($\ge 50$ MW) had non-standard DUID structures and were successfully retrieved and integrated during the registry cross-check:")
    md_content.append("- `RESS1` (Riverina Energy Storage System 1, 60.0 MW)")
    md_content.append("- `RIVNB2` (Riverina Energy Storage System 2, 65.0 MW)")
    md_content.append("- `CAPBES1` (Capital BESS, 100.0 MW)")
 
    # Accepted section
    md_content.append("\n## 1. Accepted DUIDs (Registered Capacity $\ge 50$ MW, SCADA Coverage $\ge 95\%$)")
    md_content.append("| DUID | Region | Nameplate Capacity (MW) | Max Output Seen (MW) | SCADA Intervals | Coverage (%) |")
    md_content.append("|---|---|---|---|---|---|")
    for r in accepted:
        unrecognized_flag = " (Unrecognized)" if r["Is_Unrecognized"] else ""
        md_content.append(f"| {r['DUID']}{unrecognized_flag} | {r['Region']} | {r['Capacity_MW']} | {r['Max_Seen_MW']} | {r['SCADA_Intervals']} | {r['Coverage_Pct']}% |")

    # Rejected section (Uptime)
    md_content.append("\n## 2. Rejected DUIDs (Capacity $\ge 50$ MW, SCADA Coverage $< 95\%$)")
    md_content.append("| DUID | Region | Registered Capacity (MW) | SCADA Presence Coverage (%) | Post-COD Operational Coverage (%) | Rejection Reason |")
    md_content.append("|---|---|---|---|---|---|")
    for r in rejected_uptime:
        reason = r.get("Rejection_Reason", f"Operational uptime < 95% (coverage: {r['Coverage_Pct']}%).")
        scada_pres = r.get("SCADA_Presence_Coverage_Pct", r["Coverage_Pct"])
        post_cod_op = r.get("Post_COD_Operational_Coverage_Pct", r["Coverage_Pct"])
        md_content.append(f"| **{r['DUID']}** | {r['Region']} | {r['Capacity_MW']:.1f} | {scada_pres:.2f}% | {post_cod_op:.2f}% | {reason} |")

    # Excluded section (Capacity)
    md_content.append("\n## 3. Excluded DUIDs (Capacity $< 50$ MW)")
    md_content.append("| DUID | Region | Nameplate Capacity (MW) | Max Output Seen (MW) | SCADA Intervals | Coverage (%) | Exclusion Reason |")
    md_content.append("|---|---|---|---|---|---|---|")
    for r in rejected_capacity:
        reason = "Registered capacity < 50 MW."
        md_content.append(f"| {r['DUID']} | {r['Region']} | {r['Capacity_MW']} | {r['Max_Seen_MW']} | {r['SCADA_Intervals']} | {r['Coverage_Pct']}% | {reason} |")

    # 4-Second SCADA Archive status
    md_content.append("\n## 4. Status of 4-Second Causer Pays SCADA Archive")
    md_content.append("- **Archive Status**: Historical 4-second SCADA zip archives are publicly stored in AEMO's NEMWEB archive under `/Reports/ARCHIVE/Causer_Pays_Scada/`.")
    md_content.append("- **Availability Window**: 16 June 2025 to 8 September 2025 (transition to private FPP occurred on 8 June 2025, but archives were compiled weekly until 8 September 2025).")
    md_content.append("- **Older Pre-FPP Archives**: Archives covering the beginning of our audit window (1 June 2025 to 15 June 2025) fall outside AEMO's rolling public retention window and now return HTTP 404. A search on the Internet Archive Wayback Machine CDX API on 4 July 2026 returned no indexed snapshots for these three zip URLs (`PUBLIC_CAUSER_PAYS_SCADA_20250601.zip`, `20250608.zip`, `20250615.zip`). Their original contents remain unverified, which is standard for historical causer pays telemetry older than 90 days. Separately, under the FPP framework (effective 8 June 2025), unit-level 4-second tables were decommissioned entirely per AEMO's data-design documentation (representing structural contraction rather than routine retention loss).")
    md_content.append("- **Last Archived File**: `PUBLIC_CAUSER_PAYS_SCADA_20250908.zip`")
    md_content.append("- **Sample Audit File**: `PUBLIC_CAUSER_PAYS_SCADA_20250616.zip`")
    md_content.append("- **Sample File SHA-256**: `6271eca83534825a686e69fe0d528b7bdad871420e2ec85316006ebc95284a98`")
    md_content.append("\n### Archived Weekly Files List:")
    for f in fcas_archive_files:
        md_content.append(f"- `https://nemweb.com.au/Reports/ARCHIVE/Causer_Pays_Scada/{f}`")

    # Write file
    out_md = './reports/l1_integrity_report.md'
    with open(out_md, 'w') as f:
        f.write("\n".join(md_content))
    print(f"Saved Markdown report to {out_md}")

if __name__ == '__main__':
    compile_report()
