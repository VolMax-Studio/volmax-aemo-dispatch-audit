# Explorative Analysis: AEMO Price-Quintile BESS Arbitrage

**Topic:** Daily Price-Quintile Dispatch Allocation (Stepanek Method with Charge-Side Mirroring)  
**Target Assets:** Hornsdale Power Reserve (`HPR1`, SA1) and Victorian Big Battery (`VBB1`, VIC1)  
**Timeframe:** 1 June 2025 – 31 May 2026 (12 months)  

---

## 1. Methodology & Normalization

This analysis implements and extends the daily price-ranking methodology developed by Petr Stepanek (Fingrid) to investigate BESS strategic dispatch allocation in the Australian National Electricity Market (NEM).

1. **Daily Normalization (Relative vs. Absolute)**:
   For each day, the 288 five-minute settlement intervals are ranked based on their Regional Reference Price (`RRP`). The day is divided into five equal-sized quintiles (each representing exactly 20% of the day, or ~4.8 hours):
   * **Q5 (Most Expensive)**: Top 20% priced intervals of the day.
   * **Q4 / Q3 / Q2**: Intermediate price tiers.
   * **Q1 (Cheapest)**: Bottom 20% priced intervals of the day.
   
   This relative daily ranking neutralizes seasonal shifts and absolute price level swings, making different months directly comparable.

2. **Charge-Side Mirroring**:
   While the Fingrid baseline analysis only looked at the discharge side (generation), AEMO's per-unit data is fully bidirectional. We compute both:
   * **Discharge Share**: Percentage of monthly discharge energy (MWh) occurring in each price quintile.
   * **Charge Share**: Percentage of monthly charge energy (MWh) occurring in each price quintile.

3. **Arbitrage Maturity Signal**:
   * *Random / Non-arbitrage Baseline*: $\approx 20\%$ energy share across all five quintiles.
   * *Arbitrage Concentration*: Discharge concentrates in **Q5** and charge concentrates in **Q1**.

4. **FCAS & Telemetry Caveats (Operational Boundaries)**:
   * **FCAS Contamination**: SCADA active power (`SCADAVALUE`) is the sum of energy arbitrage and enabled FCAS response. Contingency FCAS active power response is not separated in this dataset. However, because high-power dispatch events dominate energy volume, the overall monthly energy allocation reflects bulk energy behavior, while standby and regulation noise are secondary.
   * **Standby Threshold**: We apply a $\pm0.1\text{ MW}$ standby threshold. Active power within this band is treated as idle, though in reality it may contain low-amplitude frequency regulation signals.

---

## 2. Key Findings & Asymmetric Trend

Our analysis reveals an **asymmetric operational signature**: a clear charge-side concentration trend, contrasted with a flat, noisy discharge-side concentration.

### Monthly Results Summary

| Month | HPR1 Spread ($) | HPR1 Disch Q5 | HPR1 Charge Q1 | VBB1 Spread ($) | VBB1 Disch Q5 | VBB1 Charge Q1 |
|:---|---:|---:|---:|---:|---:|---:|
| **2025-06** | $741 | 49.8% | 46.4% | $786 | 54.9% | 41.9% |
| **2025-07** | $468 | 39.3% | 38.4% | $161 | 60.3% | 45.8% |
| **2025-08** | $190 | 52.8% | 46.4% | $182 | 61.7% | 53.8% |
| **2025-09** | $174 | 45.4% | 53.3% | $159 | 47.9% | 49.3% |
| **2025-10** | $171 | 40.8% | 54.8% | $147 | 48.2% | 47.7% |
| **2025-11** | $154 | 41.3% | 50.0% | $131 | 39.5% | 57.8% |
| **2025-12** | $208 | 35.0% | 54.2% | $121 | 46.8% | 59.3% |
| **2026-01** | $685 | 39.9% | 55.2% | $120 | 48.0% | 52.5% |
| **2026-02** | $177 | 37.9% | 58.9% | $96 | 49.0% | 61.4% |
| **2026-03** | $149 | 44.8% | 63.9% | $89 | 43.9% | 56.2% |
| **2026-04** | $124 | 48.5% | 60.4% | $90 | 55.1% | 48.0% |
| **2026-05** | $84 | 35.9% | 46.8% | $77 | 45.5% | 38.5% |

*Note on Data Consistency: The summary values above are monthly total energy aggregates (sum of all energy per quintile divided by monthly total energy). The volatility control tables below are averaged from daily ratios, which introduces minor differences in absolute shares due to day-level weighting.*

### Analysis

1. **Discharge Side: Noisy Baseline (No Trend)**:
   The percentage of discharge energy in the most expensive quintile (Q5) shows no clear trend over time. It fluctuates noisily between **35% and 53%** for HPR1, and between **39% and 62%** for VBB1. While this is significantly above the 20% random baseline (indicating consistent arbitrage intent), it remains stationary around its mean.
   
2. **Charge Side: High-Level Trend**:
   In contrast, the charge-side allocation in Q1 (cheapest) shows a distinct upward shift from winter (June–July 2025) through autumn (March 2026):
   * **HPR1** Q1 charge share rises from **46.4%** in June 2025 (or **38.4%** in July 2025, which represents the lowest monthly average) to a peak of **63.9%** in March 2026, before declining in late autumn (May 2026). Depending on the choice of baseline month, this represents an increase of **14 to 26 percentage points** to the peak.
   * **VBB1** Q1 charge share rises from **41.9%** in June 2025 to a peak of **61.4%** in February 2026, before dropping.
   
   This rise in Q1 charge concentration occurred while the monthly average price spread fell from over $700/MWh to sub-$100/MWh.

---

## 3. Volatility Control (Eliminating the Flat-Day Artifact)

An alternative hypothesis is that the rising Q1 charge share is a mathematical artifact of declining price volatility. On low-volatility days, price curves are flatter, and minor deviations can easily cluster charging data into Q1.

To test this, we bin daily price spreads (Daily Spread = $\text{Mean}(RRP_{Q5}) - \text{Mean}(RRP_{Q1})$) and calculate the average Q1 charge share for days belonging to the same spread bin. We display the sample size ($n$ = number of days in the cell) to control for small-sample noise.

### HPR1 (SA1): Monthly Average Q1 Charge Share by Daily Price Spread Bin

| Month | Spread \$50 – \$150 | Spread \$150 – \$300 | Spread \$300+ |
|:---|---:|---:|---:|
| **2025-06** | 46.9% (n=14) | 51.6% (n=9) | 35.7% (n=6) |
| **2025-07** | 40.2% (n=5) | 39.4% (n=23) | 34.1% (n=3) |
| **2025-08** | 42.8% (n=7) | 46.5% (n=22) | 63.0% (n=2) |
| **2025-09** | 54.4% (n=12) | 53.6% (n=16) | 71.3% (n=2) |
| **2025-10** | 51.9% (n=9) | 56.6% (n=20) | - |
| **2025-11** | 48.3% (n=15) | 52.2% (n=14) | - |
| **2025-12** | 56.6% (n=10) | 54.0% (n=18) | 48.2% (n=3) |
| **2026-01** | 55.0% (n=17) | 60.2% (n=8) | 50.8% (n=6) |
| **2026-02** | 53.8% (n=10) | 60.5% (n=16) | 48.2% (n=2) |
| **2026-03** | 61.4% (n=15) | 65.8% (n=15) | - |
| **2026-04** | 58.9% (n=18) | 62.7% (n=9) | - |
| **2026-05** | 44.8% (n=23) | - | - |

**Verdict (HPR1)**: Within the highly populated **Spread \$150 – \$300** bin (where cell sample sizes range from $n=8$ to $n=23$), the Q1 charge share rises from **51.6%** (June) / **39.4%** (July) to **65.8%** (March) / **62.7%** (April). The same upward trend is visible in the **Spread \$50 – \$150** bin. This confirms that **the charge-side concentration shift for HPR1 is not a mathematical artifact of shifting spread levels.**

### VBB1 (VIC1): Monthly Average Q1 Charge Share by Daily Price Spread Bin

| Month | Spread \$50 – \$150 | Spread \$150 – \$300 |
|:---|---:|---:|
| **2025-06** | 47.2% (n=12) | 40.3% (n=12) |
| **2025-07** | 45.2% (n=12) | 46.9% (n=19) |
| **2025-08** | 58.0% (n=12) | 55.2% (n=17) |
| **2025-09** | 57.2% (n=15) | 44.6% (n=14) |
| **2025-10** | 45.1% (n=13) | 45.8% (n=16) |
| **2025-11** | 54.2% (n=18) | 64.2% (n=11) |
| **2025-12** | 59.7% (n=25) | 66.9% (n=6) |
| **2026-01** | 54.9% (n=26) | 34.2% (n=1) |
| **2026-02** | 60.5% (n=24) | 72.0% (n=2) |
| **2026-03** | 57.6% (n=26) | - |
| **2026-04** | 50.7% (n=24) | 56.9% (n=1) |
| **2026-05** | 43.6% (n=23) | 18.5% (n=2) |

**Verdict (VBB1)**: For VBB1, the results are mixed:
*   In the **Spread \$50 – \$150** bin (highly populated with $n \ge 12$ days per month), the Q1 charge share exhibits a stable upward trend peaking in February at **60.5%** and March at **57.6%** before dropping.
*   In the **Spread \$150 – \$300** bin, the cell counts collapse starting in January 2026 ($n \le 2$ days per month) due to Victoria's price spread compression. Consequently, the wild fluctuations observed (e.g. dropping to 34% in Jan and surging to 72% in Feb) represent small-sample noise rather than a meaningful physical signal.
*   *Conclusion*: VBB1's trend is only robustly confirmed within its lower price volatility range.

---

## 4. Statistical Significance Test (Linear Regression)

To quantitatively evaluate if the charge-side trends are statistically significant, we fit an ordinary least squares (OLS) linear regression of daily Q1 charge share ($Y$) on time ($X$, in days since June 1, 2025) for each asset's key spread bins.

### Regression Results (Daily Data)

1. **HPR1 (SA1)**:
   *   **Spread \$150 – \$300 Bin (n = 170 days)**:
       *   *Monthly Slope*: **+2.18 percentage points per month**
       *   *Coefficient of Determination ($R^2$)*: **0.1448**
       *   *p-value*: **< 0.000001**
       *   *Verdict*: **STATISTICALLY SIGNIFICANT**. There is a strong, highly significant positive trend.
   *   **Spread \$50 – \$150 Bin (n = 155 days)**:
       *   *Monthly Slope*: **+0.54 percentage points per month**
       *   *p-value*: **0.2497**
       *   *Verdict*: **NOT SIGNIFICANT**. The upward trend is not statistically distinguishable from random variation.

2. **VBB1 (VIC1)**:
   *   **Spread \$50 – \$150 Bin (n = 230 days)**:
       *   *Monthly Slope*: **+0.04 percentage points per month**
       *   *p-value*: **0.9222**
       *   *Verdict*: **NOT SIGNIFICANT**. The daily charge share is statistically flat over the year.
   *   **Spread \$150 – \$300 Bin (n = 101 days)**:
       *   *Monthly Slope*: **+1.09 percentage points per month**
       *   *p-value*: **0.1244**
       *   *Verdict*: **NOT SIGNIFICANT**. Positive slope is observed but fails to reach the $\alpha = 0.05$ significance threshold.

### Summary
The statistical check reveals that **only HPR1's charge concentration in the moderate price spread range (\$150–\$300) represents a statistically significant positive trend.** VBB1's charge concentration shifts, as well as both units' low-spread shifts, are not statistically distinguishable from random noise. The maturation narrative is therefore limited solely to HPR1 under moderate volatility conditions.

---

## 5. Alternative Hypothesis: Shifting Price Curve Shape (Solar Penetration)

While the daily spread control demonstrates that the HPR1 moderate-spread trend is not an artifact of the spread *magnitude*, it does not prove algorithmic/strategic maturation by the BESS operator.

An alternative explanation is **price curve shape evolution**:
*   Over the audit period, South Australia and Victoria experienced increased utility and rooftop solar penetration.
*   This solar influx deepens and widens the midday price trough, creating a highly predictable, multi-hour "solar valley" where prices are consistently locked at or near zero.
*   A wider and more predictable midday low-price window makes it easier for a battery system to concentrate its charging in Q1, even if it uses a simple, static scheduling strategy.

Because our daily price ranking only normalizes the *rank* and not the *shape* of the daily price curve, we cannot distinguish between a battery getting "smarter" (algorithmic optimization) and the price curve getting "easier" (wider low-price valleys). This remains an open research question.

---

## 6. Generated Visualizations

The generated stacked-area charts show the full quintile distributions across the 12-month window:

*   **Hornsdale Power Reserve (HPR1) Chart**: [hpr1_quintile_share.png](file:///home/volmax-studio/volmax-projects/iot2/PORTFOLIO/volmax-aemo-dispatch-audit/analysis/quintile_exploration/results/hpr1_quintile_share.png)
*   **Victorian Big Battery (VBB1) Chart**: [vbb1_quintile_share.png](file:///home/volmax-studio/volmax-projects/iot2/PORTFOLIO/volmax-aemo-dispatch-audit/analysis/quintile_exploration/results/vbb1_quintile_share.png)

*(Note: In the discharge plots, the Q5 red layer is at the top; in the charge plots, the Q1 blue layer is at the bottom.)*
