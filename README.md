# AEMO BESS Fleet Dispatch Audit

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21190094.svg)](https://doi.org/10.5281/zenodo.21190094)

Independent fleet-wide audit of grid-scale battery energy storage systems (BESS) operating in the Australian National Electricity Market (NEM) from **June 1, 2025 to May 31, 2026**.

---

## 1. Audit Limitations & Structural Boundaries

Under the VolMax P10 Verification Protocol, this audit operates under several physical, institutional, and data-resolution limitations that constrain public auditability:

### 1.1 FPP Informational Contraction (Unit-Level SCADA Deletion)
Following the transition to the Frequency Performance Payments (FPP) framework on **8 June 2025**, AEMO ceased publishing unit-level 4-second SCADA active power telemetry. A review of AEMO public archives shows that the `INDIVIDUAL` and `UNIT` telemetry tables were completely stripped.
- **Impact**: Sub-minute FCAS physical response is participant-private. The claim **ES-AU-03 (FCAS response verification)** is **Unfalsifiable / Not Publicly Auditable** for the entire audit window. Event analysis must rely on 5-minute SCADA averages, smoothing out high-frequency response.

### 1.2 Purged Pre-FPP Archives (404 Errors & Wayback Machine Check)
The three weekly archives covering the pre-FPP weeks (June 1–15, 2025) are completely missing from AEMO's NEMWEB servers, returning HTTP 404 errors:
- `PUBLIC_CAUSER_PAYS_SCADA_20250601.zip` (404)
- `PUBLIC_CAUSER_PAYS_SCADA_20250608.zip` (404)
- `PUBLIC_CAUSER_PAYS_SCADA_20250615.zip` (404)
A search of the Internet Archive Wayback Machine CDX API on 4 July 2026 returned no indexed snapshots for these three zip URLs, meaning they are not recoverable from public sources. `PUBLIC_CAUSER_PAYS_SCADA_20250616.zip` is the earliest available archive on NEMWEB but contains stripped post-FPP tables.

### 1.3 Standby Resolution Confound
Resampling 5-minute SCADA telemetry to 15-minute averages introduces a negative standby ratio confound of **$-3.95$ percentage points** (dropping from $9.27\%$ to $5.32\%$, dynamically calculated on `HPR1` data) because short active spikes contaminate adjacent idle blocks.
- **Generalization Impact**: If the same mechanism holds for the European ECO STOR Bollingstedt battery (n=1 reference, calculated at 15-minute resolution), its $60\%$ standby ratio is a conservative **lower bound** of its true idle state. This makes the contrast with the active Australian fleet (where standby ratios under $30\%$ and daily EFCs of 1.0–1.5 dominate) even more pronounced.

### 1.4 Registry Cross-Check & Exclusions
The candidate pool was cross-checked against the official **AEMO Generation Information (April 2026)** list. Candidates failing to meet the $95\%$ SCADA uptime threshold or under commissioning during the audit window are logged in the L1 report and excluded from downstream analysis. 
- **Thermal Leaks Stripped**: `LOYYB1` (Loy Yang B Unit 1 coal, 510 MW) and `TORRB1` (Torrens Island B Unit 1 gas, 200 MW) were successfully stripped.
- **Commissioning Exclusions**: `WTAHB1` (Waratah Super Battery, prolonged transformer issues), `TARBESS1` (Tarong BESS, COD 15 Feb 2026), `TEMPB1` (Templers BESS, COD 1 Mar 2026), and `LDLL1` (Liddell Battery, COD mid-2026) are rejected.
- **A-Priori Fleet Rules (KESSB1)**: Koorangie BESS (`KESSB1`, COD 1 August 2025) fails the a-priori selection rule ($\ge 95\%$ coverage over 12 months, maximum possible coverage $\approx 83\%$) and is rejected from the primary fleet baseline; its post-COD performance is evaluated separately in the Level 2 report Appendix.

---

## 2. Pinned Licensing & Copyright Terms
- **Source**: AEMO Privacy and Legal Notices (https://aemo.com.au/privacy-and-legal-notices)
- **Accessed Date**: 2026-07-03
- **AEMO Permission Wording**:
  > *"In addition to the use of AEMO Material permitted under the Copyright Act 1968 (Cth), AEMO grants you a general permission to use AEMO Material for any purpose, provided that you give an accurate and appropriate attribution to the material and to AEMO as the author. Specific permission is not required for such use."*
- **Application**: The raw market datasets (`DISPATCH_UNIT_SCADA`, `DISPATCHLOAD`, `DISPATCHPRICE`) are sourced directly from AEMO's public NEMWEB portal and compiled with appropriate attribution. Raw data is not redistributed in this repository; instead, the download pipeline re-fetches raw files directly from AEMO and verifies them against pinned SHA-256 hashes in `data_manifest.json`.

---

## 3. A-Priori Fleet Selection Rule (IESS-Aligned)
To prevent data curation bias, BESS units are selected for this audit based on the following strict, neutral criteria:
1. **Capacity**: The battery asset must have a registered nameplate capacity of $\ge 50\text{ MW}$ (for either its charging load or discharging generation) according to the **AEMO Generation Information Page** (referenced snapshot: **April 2026**). This includes:
   - Single bidirectional units (IRP / BDU, e.g., `HPR1`, `VBB1`), and
   - Legacy Generation/Load pairs (treated as a single asset, e.g., `G1` and `L1`).
2. **Operational Window**: The asset must have active SCADA coverage of $\ge 95\%$ of intervals in the 12-month audit window (**June 1, 2025 to May 31, 2026**).
3. **Exclusions / Commissioning Amendment**: Any unit meeting the capacity threshold but failing the operational window criteria will be logged in the L1 report with an explicit rejection reason (e.g., commissioned mid-window or data gaps). Under the commissioning review amendment (amended before final analysis per commissioning review), units whose commercial operation date falls inside the window are rejected regardless of SCADA presence.

---

## 4. Claims Ledger (ES-AU)

### [ES-AU-01] Dispatch Conformance Target
- **Source Claim**: National Electricity Rules Clause 4.9.8 (Generator to comply with dispatch instructions - National Electricity Rules Version 200, accessed July 2026).
- **Audit Target**: Compare the 5-minute target dispatch (field `TOTALCLEARED` in the `DISPATCHLOAD` table) against actual 5-minute SCADA power output (field `SCADAVALUE` in `DISPATCH_UNIT_SCADA`).
- **Semantic Alignment Justification**: 
  - Over 3,756,657 records in June 2025, we verified that `SCADAVALUE(t) ≡ INITIALMW(t)` with a $100.00\%$ match rate.
  - Per the AEMO MMS Data Model, `INITIALMW(t)` represents the active power at the *start* of interval $t$ (time $t-5$).
  - Therefore, the actual power at the *end* of interval $t$ is recorded as `SCADAVALUE(t+5)` (or `INITIALMW(t+5)`).
  - The audit compares `SCADAVALUE(t+5)` (actual end value) against `TOTALCLEARED(t)` (end target).
- **Verdict**: **Verified (with Descriptive Band)**. Conformance within the VolMax descriptive band ($\max(6\text{ MW}, 3\%\text{ capacity})$) is verified at 5-minute resolution; **this is not a regulatory compliance determination under NER 4.9.8**.
- **Verifiable Metric**: 
  - Root Mean Square Error (RMSE) and Mean Absolute Error (MAE) of dispatch deviation per battery.
  - Exceedance rate: Percentage of intervals violating the **VolMax Descriptive Conformance Band** ($\max(6\text{ MW}, 3\%\text{ of nameplate capacity})$).

### [ES-AU-02] Cross-Jurisdictional Generalization
- **Source Claim**: VolMax hypothesis (from ECO STOR audit): compliance/regime signatures observed on one European asset generalize across fleets.
- **Audit Target**: Compare dispatch noise patterns, cycle durations, and standby regimes between Australian batteries (AEMO) and our single-asset European reference (ECO STOR audit, n=1).
- **Verdict**: **Not Verified (Hypothesis Rejected)**. Australian BESS operational signatures (standby $<30\%$, EFC 1.0–1.5) differ drastically from the European reference (standby $\approx 60\%$, EFC 0.5–0.7). Operational signatures are market-specific and do not transfer.
- **Verifiable Metric**:
  - Standby ratio: Percentage of time battery power output is within $\pm 0.1\text{ MW}$ (inactive).
  - Equivalent Full Cycles (EFC) per day.
  - Sub-MW variance: Standard deviation of 5-minute dispatch power changes during active periods.

### [ES-AU-03] Hornsdale Power Reserve FCAS Performance
- **Source Claim**: Neoen / Tesla claim that the Hornsdale Power Reserve (HPR) provides instant frequency response to grid frequency deviations (FCAS).
- **Audit Findings & Verdict**:
  - **Verdict**: **Unfalsifiable / Not Publicly Auditable**. Unit-level response is not publicly auditable for the entire window due to FPP-led public unit SCADA decommissioning; hybrid analysis of the active window is consistent with frequency-response-driven deviations.
  - **Unit-Level 4s Response**: Not publicly auditable for the entire window; hybrid analysis only (4s network frequency × 5-min unit SCADA, 15 June – 11 September 2025 [1]).
  - **Grid Volatility Correlation**: Target deviations show a positive correlation with grid frequency volatility ($r$ ranges from $-0.0175$ to $+0.1162$ across the fleet). Volatility during conformance exceedance intervals is higher, with a fleet-wide median increase of **$+6.46\%$** (e.g. up to **$31.23\%$ higher** for `CAPBES1`). This is consistent with frequency-response-driven deviations where BESS units deviate from 5-minute targets to physically respond to sub-second frequency excursions.

---

## 5. How to Reproduce & Verify

To run the end-to-end audit (data preparation, hash verification, Level 1, Level 2, and Level 3 reports/plots generation) on a clean workspace, run:

```bash
python reproduce.py
```

### Generated Artifacts
- **L1 Report**: [l1_integrity_report.md](l1_integrity_report.md)
- **L2 Report**: [l2_conformance_report.md](l2_conformance_report.md)
- **L3 Report**: [l3_fcas_report.md](l3_fcas_report.md)
- **Plots**:
  - Conformance Exceedance Rates: `./results/plot1_conformance_exceedance.png`
  - EFC vs Standby Scatter: `./results/plot2_efc_vs_standby.png`
  - 4s Grid Freq vs 5m BESS Output: `./results/plot3_fcas_event_august19.png`
- **Data Manifest**: `./data/data_manifest.json` (SHA-256 integrity map)

---

## 6. Footnotes
[1] The Causer Pays SCADA weekly zip archives follow a filename convention where the date in the filename represents the approximate start of the week that the file covers (e.g., `PUBLIC_CAUSER_PAYS_SCADA_20250616.zip` begins coverage on 2025-06-15 23:35 market time). The final archive `PUBLIC_CAUSER_PAYS_SCADA_20250908.zip` was cut off mid-week on **2025-09-11 15:00 AEST**, which represents the precise gašenja (shutdown) timestamp when AEMO ceased publishing this telemetry publicly.
