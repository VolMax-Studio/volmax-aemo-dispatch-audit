One significant regression out of six. And even that one is subject to alternative explanations.

We took the daily price-quintile dispatch ranking method (borrowed from a recent Fingrid analysis by Petr Stepanek) and extended it with a charge-side mirror, since AEMO publishes fully bidirectional telemetry. We applied this stress-test to two major Australian assets — Hornsdale Power Reserve (HPR1) and Victorian Big Battery (VBB1) — over a 12-month window (June 2025 – May 2026).

We expected to verify a dual-sided "maturation" of arbitrage behavior: discharge shifting to the daily top-priced quintile (Q5) and charge shifting to the daily bottom-priced quintile (Q1). 

Here is what the statistics actually show when stress-tested:

1. The Discharge Side is Stationary
Discharge energy concentrates in high-price intervals (consistent with arbitrage, though active FCAS response is not separated in this telemetry), but it fluctuates noisily around a stationary mean (35%–53% for HPR1, 39%–62% for VBB1) without operational maturation over the year.

2. The Charge Side is Asymmetric and Volatility-Sensitive
While visual stacked area charts suggest a rising Q1 charge share, controlling for daily price spread (volatility) collapses the trend for one of the assets:
— Victorian Big Battery (VBB1): We see no statistically significant trend. In the highly populated low-spread bin ($50–$150/MWh, n = 230 days), the daily charge share is statistically flat (slope +0.04 pp/month, p = 0.92). In the moderate-spread bin ($150–$300/MWh), price spread compression starting January 2026 reduced sample sizes to only 1–2 days per month, rendering OLS trends in that range uninterpretable noise.
— Hornsdale Power Reserve (HPR1): In the moderate spread bin ($150–$300/MWh, n = 170 days), the trend is statistically significant. The Q1 charge share rises from 51.6% in June 2025 (or 39.4% in July 2025) to a peak of 65.8% in March 2026. Depending on the baseline month chosen, this represents a 14 to 26 percentage point increase. The daily linear regression slope is +2.18 percentage points per month (R² = 0.14, p < 0.000001 — a statistically significant positive slope, though the low R² reflects the high daily operational noise of the raw dispatch). 

3. The Solar Penetration Alternative
Even HPR1's statistically significant trend does not prove a "smarter battery." Over the audit period, increased solar penetration in South Australia deepened and widened the midday price trough. This wider, more predictable "solar valley" makes it easier to concentrate charging in Q1, even using a simple, static scheduling strategy. 

Because daily ranking normalizes price *rank* but not price *shape*, we cannot distinguish between an algorithm getting smarter and the price curve getting easier.

In deep tech auditing, we lead with limitations. The full code, the data stitching registry, the monthly stacked-area plots, and the 2x2 daily OLS regression panels are open-source and open-data.

Links to the exploration branch and full results are in the first comment.

#BESS #EnergyStorage #ElectricityMarkets #GridStorage #OpenData #VolMaxStudio
