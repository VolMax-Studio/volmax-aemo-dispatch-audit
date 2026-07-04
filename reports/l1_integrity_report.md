# L1 Integrity Report - AEMO BESS Fleet Audit

Audit Window: **1 June 2025 to 31 May 2026** (105120 expected 5-minute intervals per unit)

> [!NOTE]
> **Audit Window Adjustment**: The audit window represents a complete 12-month annual cycle. Data for June 2026 was excluded because AEMO's monthly MMSDM SQL loader archive file for June 2026 has not yet been released in the public directory (typically published around the 10th-15th of the following month).

## Candidate Pool Construction & Audit Provenance
To ensure absolute compliance with the P10 protocol, the BESS candidate pool was constructed and verified through a two-stage process:
1. **DUID Name-Pattern Matching**: Initial candidates were gathered by scanning historical AEMO SCADA telemetry for units with DUIDs matching typical battery suffixes (`B1`, `B2`, `BESS`, `BATTERY`).
2. **Official Registry Cross-Check**: The extracted candidates were cross-referenced against the official **AEMO Generation Information (April 2026)** spreadsheet to map all operating energy storage systems $\ge 50$ MW.

### Thermal Unit Exclusions (Leaks)
The following thermal assets were captured by the automated name-pattern search (due to suffixes like `B1` representing stage B, unit 1) but were manually verified and excluded from the battery fleet:
- `LOYYB1` (Loy Yang B Unit 1, 510 MW Coal-Fired Generator)
- `TORRB1` (Torrens Island B Unit 1, 200 MW Gas-Fired Generator)

### Non-Standard BESS DUID Additions
The following grid-scale BESS assets ($\ge 50$ MW) had non-standard DUID structures and were successfully retrieved and integrated during the registry cross-check:
- `RESS1` (Riverina Energy Storage System 1, 60.0 MW)
- `RIVNB2` (Riverina Energy Storage System 2, 65.0 MW)
- `CAPBES1` (Capital BESS, 100.0 MW)

## 1. Accepted DUIDs (Registered Capacity $\ge 50$ MW, SCADA Coverage $\ge 95\%$)
| DUID | Region | Nameplate Capacity (MW) | Max Output Seen (MW) | SCADA Intervals | Coverage (%) |
|---|---|---|---|---|---|
| BBATTERY1 | QLD1 | 50.0 | 50.05 | 105120 | 100.0% |
| BHB1 | NSW1 | 50.0 | 49.96 | 105120 | 100.0% |
| BLYTHB1 | SA1 | 281.0 | 201.49 | 105120 | 100.0% |
| CAPBES1 | NSW1 | 100.0 | 101.67 | 105120 | 100.0% |
| CHBESS1 | QLD1 | 100.0 | 100.06 | 105120 | 100.0% |
| HBESS1 | VIC1 | 200.0 | 153.4 | 105120 | 100.0% |
| HPR1 | SA1 | 150.0 | 92.0 | 105120 | 100.0% |
| RANGEB1 | VIC1 | 260.0 | 202.78 | 105120 | 100.0% |
| RESS1 | NSW1 | 60.0 | 60.61 | 105120 | 100.0% |
| RIVNB2 | NSW1 | 65.0 | 65.61 | 105120 | 100.0% |
| TIB1 | SA1 | 250.0 | 251.23 | 105120 | 100.0% |
| ULPBESS1 | NSW1 | 52.0 | 155.3 | 104544 | 99.452% |
| VBB1 | VIC1 | 360.0 | 300.9 | 105120 | 100.0% |
| WALGRV1 | NSW1 | 50.0 | 51.03 | 105120 | 100.0% |
| WANDB1 | QLD1 | 123.0 | 100.45 | 105120 | 100.0% |
| WDBESS1 | QLD1 | 255.0 | 256.64 | 105120 | 100.0% |

## 2. Rejected DUIDs (Capacity $\ge 50$ MW, SCADA Coverage $< 95\%$)
| DUID | Region | Registered Capacity (MW) | SCADA Presence Coverage (%) | Post-COD Operational Coverage (%) | Rejection Reason |
|---|---|---|---|---|---|
| **KESSB1** | VIC1 | 185.0 | 100.00% | 83.29% | Commissioned mid-window (COD: 1 August 2025). Post-COD operational coverage is 83.29%, failing the a-priori selection rule. |
| **LDLL1** | NSW1 | 500.0 | 0.00% | 0.00% | Under testing/commissioning throughout the audit window (commercial operations started mid-2026; no SCADA output in our audit window). |
| **TARBESS1** | QLD1 | 393.0 | 100.00% | 29.04% | Commissioned mid-window (COD: 15 Feb 2026). Post-COD operational coverage is 29.04%, failing the a-priori selection rule. |
| **TEMPB1** | SA1 | 111.0 | 100.00% | 25.20% | Commissioned mid-window (COD: 1 Mar 2026). Post-COD operational coverage is 25.21%, failing the a-priori selection rule. |
| **WTAHB1** | NSW1 | 1096.0 | 100.00% | 0.00% | Under testing/commissioning throughout the 12-month window due to prolonged transformer issues (no commercial operation date). |

## 3. Excluded DUIDs (Capacity $< 50$ MW)
| DUID | Region | Nameplate Capacity (MW) | Max Output Seen (MW) | SCADA Intervals | Coverage (%) | Exclusion Reason |
|---|---|---|---|---|---|---|
| BALB1 | VIC1 | 30.0 | 30.67 | 105120 | 100.0% | Registered capacity < 50 MW. |
| BRYB1WF1 | VIC1 | 20.0 | 175.6 | 105120 | 100.0% | Registered capacity < 50 MW. |
| DPNTB1 | NSW1 | 25.0 | 25.35 | 105120 | 100.0% | Registered capacity < 50 MW. |
| GANNB1 | VIC1 | 25.0 | 26.25 | 105120 | 100.0% | Registered capacity < 50 MW. |
| GREENB1 | WA1 | 5.0 | 200.93 | 105120 | 100.0% | Registered capacity < 50 MW. |
| GSWF1B1 | NSW1 | 10.0 | 199.3 | 105120 | 100.0% | Registered capacity < 50 MW. |
| LBB1 | SA1 | 25.0 | 25.05 | 105120 | 100.0% | Registered capacity < 50 MW. |
| MANNUMB1 | SA1 | 30.0 | 107.27 | 105120 | 100.0% | Registered capacity < 50 MW. |
| PIBESS1 | SA1 | 5.0 | 5.33 | 105120 | 100.0% | Registered capacity < 50 MW. |
| QBYNB1 | NSW1 | 8.0 | 10.04 | 105120 | 100.0% | Registered capacity < 50 MW. |
| TALWB1 | SA1 | 41.5 | 322.2 | 105120 | 100.0% | Registered capacity < 50 MW. |
| TB2B1 | SA1 | 41.5 | 41.5 | 105120 | 100.0% | Registered capacity < 50 MW. |

## 4. Status of 4-Second Causer Pays SCADA Archive
- **Archive Status**: Historical 4-second SCADA zip archives are publicly stored in AEMO's NEMWEB archive under `/Reports/ARCHIVE/Causer_Pays_Scada/`.
- **Availability Window**: 16 June 2025 to 8 September 2025 (transition to private FPP occurred on 8 June 2025, but archives were compiled weekly until 8 September 2025).
- **Older Pre-FPP Archives**: Archives covering the beginning of our audit window (1 June 2025 to 15 June 2025) fall outside AEMO's rolling public retention window and now return HTTP 404. A search on the Internet Archive Wayback Machine CDX API on 4 July 2026 returned no indexed snapshots for these three zip URLs (`PUBLIC_CAUSER_PAYS_SCADA_20250601.zip`, `20250608.zip`, `20250615.zip`). Their original contents remain unverified, which is standard for historical causer pays telemetry older than 90 days. Separately, under the FPP framework (effective 8 June 2025), unit-level 4-second tables were decommissioned entirely per AEMO's data-design documentation (representing structural contraction rather than routine retention loss).
- **Last Archived File**: `PUBLIC_CAUSER_PAYS_SCADA_20250908.zip`
- **Sample Audit File**: `PUBLIC_CAUSER_PAYS_SCADA_20250616.zip`
- **Sample File SHA-256**: `6271eca83534825a686e69fe0d528b7bdad871420e2ec85316006ebc95284a98`

### Archived Weekly Files List:
- `https://nemweb.com.au/Reports/ARCHIVE/Causer_Pays_Scada/PUBLIC_CAUSER_PAYS_SCADA_20250616.zip`
- `https://nemweb.com.au/Reports/ARCHIVE/Causer_Pays_Scada/PUBLIC_CAUSER_PAYS_SCADA_20250623.zip`
- `https://nemweb.com.au/Reports/ARCHIVE/Causer_Pays_Scada/PUBLIC_CAUSER_PAYS_SCADA_20250630.zip`
- `https://nemweb.com.au/Reports/ARCHIVE/Causer_Pays_Scada/PUBLIC_CAUSER_PAYS_SCADA_20250707.zip`
- `https://nemweb.com.au/Reports/ARCHIVE/Causer_Pays_Scada/PUBLIC_CAUSER_PAYS_SCADA_20250714.zip`
- `https://nemweb.com.au/Reports/ARCHIVE/Causer_Pays_Scada/PUBLIC_CAUSER_PAYS_SCADA_20250721.zip`
- `https://nemweb.com.au/Reports/ARCHIVE/Causer_Pays_Scada/PUBLIC_CAUSER_PAYS_SCADA_20250728.zip`
- `https://nemweb.com.au/Reports/ARCHIVE/Causer_Pays_Scada/PUBLIC_CAUSER_PAYS_SCADA_20250804.zip`
- `https://nemweb.com.au/Reports/ARCHIVE/Causer_Pays_Scada/PUBLIC_CAUSER_PAYS_SCADA_20250811.zip`
- `https://nemweb.com.au/Reports/ARCHIVE/Causer_Pays_Scada/PUBLIC_CAUSER_PAYS_SCADA_20250818.zip`
- `https://nemweb.com.au/Reports/ARCHIVE/Causer_Pays_Scada/PUBLIC_CAUSER_PAYS_SCADA_20250825.zip`
- `https://nemweb.com.au/Reports/ARCHIVE/Causer_Pays_Scada/PUBLIC_CAUSER_PAYS_SCADA_20250901.zip`
- `https://nemweb.com.au/Reports/ARCHIVE/Causer_Pays_Scada/PUBLIC_CAUSER_PAYS_SCADA_20250908.zip`