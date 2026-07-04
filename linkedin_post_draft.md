# LinkedIn Post Draft: AEMO BESS Fleet Dispatch & Generalization Audit

Our hypothesis failed. 

When we began auditing battery energy storage system (BESS) operational behaviors in the Australian National Electricity Market (NEM), we expected to see operational signatures similar to our European reference asset (the ECO STOR Bollingstedt battery). 

They do not generalize. The Australian fleet operates under a fundamentally different regime:
* **The Generalization Gap**: The European reference battery shows a standby ratio of ~60% and cycles 0.5–0.7 times per day. In contrast, the active Australian fleet is cycled roughly 2–3× harder (EFC 1.0–1.5 vs. 0.5–0.7, standby under 30% vs. 60%). Operational signatures are highly market-specific and do not transfer.
* **The Telemetry Transparency Gap**: While cross-checking these signatures across 16 major BESS assets (nameplate capacity ≥ 50 MW, SCADA uptime ≥ 95%), we audited unit-level responses to grid frequency excursions. We found that the public window for unit-level sub-minute verification has closed. Following the transition to the Frequency Performance Payments (FPP) framework, AEMO decommissioned public unit-level 4-second SCADA. The 4-second network frequency telemetry itself remained publicly archived until 11 September 2025 15:00 AEST; that series has since ceased as well. High-resolution response validation is now participant-private.

Under the VolMax P10 standard, we evaluated three distinct claims for the 12-month period (1 June 2025 to 31 May 2026):

1. **[ES-AU-01] Dispatch Conformance Target**
   * **Verdict**: Verified (with Descriptive Band)
   * **Finding**: 5-minute dispatch target conformance is verified at a 5-minute resolution within our descriptive band (max(6 MW, 3% capacity)). *Note: This is a descriptive analysis and does not constitute a regulatory compliance determination under NER Clause 4.9.8.*

2. **[ES-AU-02] Cross-Jurisdictional Generalization**
   * **Verdict**: Not Verified (Hypothesis Rejected)
   * **Finding**: Australian BESS operational signatures differ drastically from the European reference, demonstrating that operational signatures do not transfer across markets.

3. **[ES-AU-03] Hornsdale Power Reserve (HPR) FCAS Performance**
   * **Verdict**: Unfalsifiable / Not Publicly Auditable
   * **Finding**: Unit-level response is not publicly auditable due to the decommissioning of public 4-second unit SCADA. However, hybrid analysis of the active window (4s network frequency × 5m unit SCADA) is consistent with frequency-response-driven deviations.

As public data granularity contracts, lenders and insurers increasingly rely on self-reported operator logs — which is precisely when independent verification of what remains public matters most.

Full audit, code, and pinned data hashes — links in the first comment.

---

### [First Comment Links]
* **Zenodo Dataset & Reports (DOI)**: [Insert Zenodo DOI Link here]
* **GitHub Repository**: https://github.com/VolMax-Studio/volmax-aemo-dispatch-audit
