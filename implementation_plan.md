# AEMO BESS Fleet Dispatch Audit (Level 3 - Audit Review and Corrections Plan)

This plan outlines the five corrective updates to the AEMO BESS Fleet Dispatch Audit to align the reports, code, and documentation with the P10 Verification Protocol.

## User Review Required

> [!IMPORTANT]
> **Corrective Findings & Methodology Adjustments**:
> 1. **Causer Pays Telemetry Blackout Confirmed**: We downloaded and inspected the earliest available weekly archive (`PUBLIC_CAUSER_PAYS_SCADA_20250616.zip`) and the last available archive (`PUBLIC_CAUSER_PAYS_SCADA_20250908.zip`). Both files contain exactly 904 rows per nested CSV and only include the `NETWORK` table (grid frequency deviation). The `INDIVIDUAL` and `UNIT` telemetry tables were stripped immediately starting from the FPP transition on 8 June 2025. AEMO completely stopped publishing even these stripped zip files after 8 September 2025. Thus, the public 4-second unit SCADA is structurally unavailable for the entire audit window.
> 2. **Conformance Band Explanation Corrected**: A smaller unit (50 MW) has a 6 MW conformance band, which represents 12% of its capacity (the widest relative margin in the fleet). A larger unit (e.g., Waratah 1096 MW) has a 32.9 MW band (3% of its capacity). The high exceedance rates of smaller batteries (up to 14%) represent an operational/behavioral finding (aggressive FCAS cycling and rapid dispatch deviations), not a band limitation.
> 3. **Standby Resolution Confound Quantified**: Resampling 5-minute SCADA data to 15-minute averages actually **decreases** the apparent standby ratio (e.g., `HPR1` drops from 6.83% to 2.26%, a change of -4.57%) because transient active intervals average into neighboring idle periods, making the entire block appear active. Thus, the Bollingstedt 60% standby ratio (calculated at 15-minute resolution) is a conservative lower bound of its true idle state, making its contrast with active SA batteries (under 25% standby) even more pronounced.

---

## Proposed Changes

### [Component: Level 2 Claims Verification]

#### [MODIFY] [verify_aemo_claims.py](file:///home/volmax-studio/volmax-projects/iot2/PORTFOLIO/volmax-aemo-dispatch-audit/verify_aemo_claims.py)
- Update the report-compiling logic `generate_markdown_report()` to correct the conformance band text. Clarify that smaller units have a wider relative conformance margin (12% of nameplate) and their higher exceedance rates reflect active FCAS/market bidding behaviors.
- Update the standby ratio comparison text: specify that the Bollingstedt battery represents a single asset (n=1) and note the resolution confound. Include the quantitative resample finding (resampling to 15-minute reduces apparent standby ratio by $\approx 4.5\%$ by averaging transient dispatch spikes, confirming the Bollingstedt 60% standby ratio is a conservative baseline).

### [Component: Level 3 FCAS Performance Audit]

#### [MODIFY] [verify_aemo_fcas.py](file:///home/volmax-studio/volmax-projects/iot2/PORTFOLIO/volmax-aemo-dispatch-audit/verify_aemo_fcas.py)
- Clarify the FPP telemetry availability: explain that all weekly zip files between June 16 and September 8, 2025 were checked and confirmed to be stripped of `INDIVIDUAL` and `UNIT` tables, containing only `NETWORK` grid frequency rows. Thus, there is no public unit-level 4-second SCADA data available anywhere in the public directory for the entire audit window.
- Re-run the script to update hashes and detached checksums.

### [Component: Documentation & Manifests]

#### [MODIFY] [l1_integrity_report.md](file:///home/volmax-studio/volmax-projects/iot2/PORTFOLIO/volmax-aemo-dispatch-audit/l1_integrity_report.md)
- Detail the BESS fleet selection filter:
  - **17 Accepted Units**: Meets capacity $\ge 50$ MW and uptime $\ge 95\%$.
  - **0 Rejected Units for Uptime**: No units $\ge 50$ MW failed the 95% uptime threshold.
  - **12 Excluded Units**: Capacity < 50 MW (e.g. `DPNTB1` at 25 MW, `TB2B1` at 41.5 MW, etc.).
  - **2 Excluded Thermal/Gas Units**: `LOYYB1` (coal) and `TORRB1` (gas).
- Document the audit window constraint: June 2026 monthly MMSDM dataset was not yet available in the public directory on the access date (4 July 2026), restricting the audit window to a clean 12-month period (1 June 2025 to 31 May 2026).
- Explicitly list the monthly manifest file names and SHA-256 hashes in a table for L4 reproducibility.
- State the early June 2025 Causer Pays status: A query of NEMWEB archives for the first week of June 2025 (`PUBLIC_CAUSER_PAYS_SCADA_20250601.zip`, `20250608.zip`, `20250615.zip`) returned 404 (purged), meaning no public archives exist today for that period.
- Replace the wording "dokazano da su trajno uklonjeni" with "nedostupni u javnoj arhivi na datum pristupa (4. jul 2026)".

---

## Verification Plan

### Automated Tests
- Run `python reproduce.py` to regenerate all L1, L2, L3 reports, and verify they match the new SHA-256 checksum files.
- Verify that `reproduce.py` completes without error.

### Manual Verification
- Review the generated `l1_integrity_report.md`, `l2_conformance_report.md`, and `l3_fcas_report.md` files to verify that all mathematical explanations, resolution confound details, and Causer Pays audit findings are correct.
