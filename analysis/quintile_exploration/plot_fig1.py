#!/usr/bin/env python3
"""
plot_fig1.py
Generates Figure 1 (Signal vs Noise) containing two scatter plots with OLS regression fits,
95% confidence intervals, and statistical annotations (slope, p-value, R2) for:
1. HPR1 Spread $150-$300 (Significant)
2. VBB1 Spread $50-$150 (Not Significant)
"""

import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from scipy import stats

processed_dir = "/home/volmax-studio/volmax-projects/iot2/PORTFOLIO/volmax-aemo-dispatch-audit/data/processed"
output_dir = "/home/volmax-studio/volmax-projects/iot2/PORTFOLIO/volmax-aemo-dispatch-audit/analysis/quintile_exploration/results"
os.makedirs(output_dir, exist_ok=True)

# Set styling for premium aesthetics
sns.set_theme(style="darkgrid")
plt.rcParams.update({
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "font.family": "sans-serif"
})

def safe_qcut(x):
    if len(x) < 5:
        return pd.Series(['Q3'] * len(x), index=x.index)
    try:
        return pd.qcut(x, q=5, labels=['Q1', 'Q2', 'Q3', 'Q4', 'Q5'])
    except Exception:
        ranks = x.rank(method='first')
        percentiles = (ranks - 1) / len(x)
        return pd.cut(percentiles, bins=[-0.1, 0.2, 0.4, 0.6, 0.8, 1.1], labels=['Q1', 'Q2', 'Q3', 'Q4', 'Q5'])

def load_data(duid, region):
    scada_files = sorted(glob.glob(os.path.join(processed_dir, "scada_*.feather")))
    price_files = sorted(glob.glob(os.path.join(processed_dir, "price_*.feather")))
    
    scada_dfs = [pd.read_feather(f)[lambda x: x['DUID'] == duid] for f in scada_files]
    scada_df = pd.concat(scada_dfs, ignore_index=True)
    
    price_dfs = [pd.read_feather(f)[lambda x: x['REGIONID'] == region] for f in price_files]
    price_df = pd.concat(price_dfs, ignore_index=True)
    
    df = pd.merge(scada_df, price_df, on='SETTLEMENTDATE', how='inner')
    df['SETTLEMENTDATE'] = pd.to_datetime(df['SETTLEMENTDATE'])
    df = df.sort_values(by='SETTLEMENTDATE').reset_index(drop=True)
    
    df['DATE'] = df['SETTLEMENTDATE'].dt.normalize()
    
    # Filter for complete days (>= 280 intervals)
    df = df.groupby('DATE').filter(lambda x: len(x) >= 280).copy()
    
    # Assign daily quintiles
    df['DAILY_PRICE_RANK'] = df.groupby('DATE')['RRP'].rank(method='first')
    df['QUINTILE'] = df.groupby('DATE')['DAILY_PRICE_RANK'].transform(safe_qcut)
    
    # Calculate daily price spread components
    daily_quintile_prices = df.groupby(['DATE', 'QUINTILE'], observed=False)['RRP'].mean().unstack()
    daily_spread = daily_quintile_prices['Q5'] - daily_quintile_prices['Q1']
    
    # Energy calculations
    df['ENERGY_MWH'] = df['SCADAVALUE'].abs() * (5.0 / 60.0)
    df['CHARGE_ENERGY'] = np.where(df['SCADAVALUE'] < -0.1, df['ENERGY_MWH'], 0.0)
    
    daily_stats = df.groupby('DATE').agg({'CHARGE_ENERGY': 'sum'}).copy()
    q_charge = df[df['QUINTILE'] == 'Q1'].groupby('DATE')['CHARGE_ENERGY'].sum()
    daily_stats['CHARGE_Q1'] = q_charge
    daily_stats['SPREAD'] = daily_spread
    
    # Filter for low throughput noise
    daily_stats = daily_stats[daily_stats['CHARGE_ENERGY'] >= 5.0].copy()
    daily_stats['CHARGE_Q1_SHARE'] = daily_stats['CHARGE_Q1'] / daily_stats['CHARGE_ENERGY']
    
    # Assign spread bins
    bins = [0, 50, 150, 300, 99999]
    labels = ['Spread_0_50', 'Spread_50_150', 'Spread_150_300', 'Spread_300_plus']
    daily_stats['SPREAD_BIN'] = pd.cut(daily_stats['SPREAD'], bins=bins, labels=labels)
    
    return daily_stats

def main():
    print("Loading HPR1 and VBB1 datasets...")
    hpr_stats = load_data("HPR1", "SA1")
    vbb_stats = load_data("VBB1", "VIC1")
    
    # Setup plotting: 1 row, 2 columns
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
    
    configs = [
        {
            "ax": ax1,
            "df": hpr_stats[hpr_stats['SPREAD_BIN'] == 'Spread_150_300'].copy(),
            "duid": "HPR1",
            "bin": "Spread $150–$300/MWh",
            "color": "#08519c",      # Dark Blue for scatter
            "line_color": "#b30000", # Red for OLS line (Significant)
            "n_label": "n = 170"
        },
        {
            "ax": ax2,
            "df": vbb_stats[vbb_stats['SPREAD_BIN'] == 'Spread_50_150'].copy(),
            "duid": "VBB1",
            "bin": "Spread $50–$150/MWh (Most Populated)",
            "color": "#3182bd",      # Medium Blue for scatter
            "line_color": "#737373", # Grey for OLS line (Not Significant)
            "n_label": "n = 230"
        }
    ]
    
    for cfg in configs:
        ax = cfg["ax"]
        bin_df = cfg["df"].dropna(subset=['CHARGE_Q1_SHARE']).sort_index()
        
        y = bin_df['CHARGE_Q1_SHARE'].values
        dates = bin_df.index
        x_num = dates.map(pd.Timestamp.toordinal).values
        n = len(bin_df)
        
        # 1. Scatter plot
        ax.scatter(dates, y, color=cfg["color"], alpha=0.5, s=35, edgecolor='none', label="Daily Data Point")
        
        # 2. Linear Regression & Stats
        slope, intercept, r_value, p_value, std_err = stats.linregress(x_num, y)
        slope_per_month = slope * 30.4
        
        # 3. Fit line and confidence bands
        x_num_range = np.linspace(x_num.min(), x_num.max(), 100)
        x_date_range = [pd.Timestamp.fromordinal(int(val)) for val in x_num_range]
        y_pred = intercept + slope * x_num_range
        
        # Standard error of prediction formulas
        # s_e: standard error of the residual
        residuals = y - (intercept + slope * x_num)
        s_e = np.sqrt(np.sum(residuals**2) / (n - 2))
        
        mean_x = np.mean(x_num)
        sum_sq_x = np.sum((x_num - mean_x)**2)
        
        # s_y0: standard error of the prediction at each point
        s_y0 = s_e * np.sqrt(1.0/n + (x_num_range - mean_x)**2 / sum_sq_x)
        
        # t-critical value for 95% confidence interval
        t_crit = stats.t.ppf(0.975, df=n-2)
        lower_band = y_pred - t_crit * s_y0
        upper_band = y_pred + t_crit * s_y0
        
        # Clip band limits to [0, 1]
        lower_band = np.clip(lower_band, 0.0, 1.0)
        upper_band = np.clip(upper_band, 0.0, 1.0)
        
        # Plot regression line
        ax.plot(x_date_range, y_pred, color=cfg["line_color"], linewidth=2.5, label="OLS Regression Fit")
        # Plot 95% confidence band
        ax.fill_between(x_date_range, lower_band, upper_band, color=cfg["line_color"], alpha=0.15, label="95% Confidence Interval")
        
        # 4. Text annotation block
        sig_text = "SIGNIFICANT" if p_value < 0.05 else "NOT SIGNIFICANT"
        p_text = f"p < 10⁻⁶" if p_value < 1e-6 else f"p = {p_value:.4f}"
        
        stat_label = (
            f"slope: {slope_per_month*100:+.2f} pp/month\n"
            f"R²: {r_value**2:.4f}\n"
            f"{p_text} ({sig_text})"
        )
        
        bbox_props = dict(boxstyle="round,pad=0.4", fc="white", ec="gray", alpha=0.9)
        ax.text(0.05, 0.95, stat_label, transform=ax.transAxes, fontsize=10, fontweight='bold' if p_value < 0.05 else 'normal',
                verticalalignment='top', bbox=bbox_props)
        
        # Title & Axis formatting
        ax.set_title(f"{cfg['duid']} charging Q1 share ({cfg['n_label']})\n{cfg['bin']}", fontweight='bold')
        ax.set_ylabel("Q1 Charge Energy Share (Cheapest 20% of Day)")
        ax.set_xlabel("Date")
        ax.set_ylim(0, 1.0)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        ax.tick_params(axis='x', rotation=30)
        ax.legend(loc='lower left')
        
    plt.tight_layout()
    fig1_path = os.path.join(output_dir, "fig1_signal_vs_noise.png")
    plt.savefig(fig1_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Figure 1 successfully saved to {fig1_path}")

if __name__ == "__main__":
    main()
