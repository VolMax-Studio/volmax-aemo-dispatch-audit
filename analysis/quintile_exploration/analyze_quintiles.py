#!/usr/bin/env python3
"""
analyze_quintiles.py
Performs Stepanek-style daily price-quintile energy allocation analysis on HPR1 and VBB1.
Generates:
1. Monthly stacked area plots of energy share (discharge/charge) by price quintile.
2. A 2x2 regression panel plot (arbitrage_regression_test.png) tracking daily Q1 charge share
   over time across key daily price spread bins, including OLS regression fits and p-values.
"""

import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
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

def load_and_preprocess(duid, region):
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
    df['MONTH'] = df['SETTLEMENTDATE'].dt.to_period('M')
    
    # Filter for complete days (>= 280 intervals)
    df = df.groupby('DATE').filter(lambda x: len(x) >= 280).copy()
    
    # Assign daily quintiles
    df['DAILY_PRICE_RANK'] = df.groupby('DATE')['RRP'].rank(method='first')
    df['QUINTILE'] = df.groupby('DATE')['DAILY_PRICE_RANK'].transform(safe_qcut)
    
    # Calculate daily price spread components
    daily_quintile_prices = df.groupby(['DATE', 'QUINTILE'], observed=False)['RRP'].mean().unstack()
    daily_spread = daily_quintile_prices['Q5'] - daily_quintile_prices['Q1']
    df['DAILY_SPREAD'] = df['DATE'].map(daily_spread)
    
    # Energy calculations
    df['ENERGY_MWH'] = df['SCADAVALUE'].abs() * (5.0 / 60.0)
    df['DISCHARGE_ENERGY'] = np.where(df['SCADAVALUE'] > 0.1, df['ENERGY_MWH'], 0.0)
    df['CHARGE_ENERGY'] = np.where(df['SCADAVALUE'] < -0.1, df['ENERGY_MWH'], 0.0)
    
    return df

def generate_monthly_plots(df, duid):
    # Aggregate monthly
    monthly_data = []
    months = sorted(df['MONTH'].unique())
    
    for m in months:
        m_df = df[df['MONTH'] == m]
        total_discharge = m_df['DISCHARGE_ENERGY'].sum()
        total_charge = m_df['CHARGE_ENERGY'].sum()
        avg_daily_spread = m_df.groupby('DATE')['DAILY_SPREAD'].first().mean()
        
        q_disch = m_df.groupby('QUINTILE', observed=False)['DISCHARGE_ENERGY'].sum()
        q_charge = m_df.groupby('QUINTILE', observed=False)['CHARGE_ENERGY'].sum()
        
        disch_shares = {q: (q_disch.get(q, 0.0) / total_discharge if total_discharge > 0 else 0.0) for q in ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']}
        charge_shares = {q: (q_charge.get(q, 0.0) / total_charge if total_charge > 0 else 0.0) for q in ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']}
        
        row = {
            "Month": str(m),
            "Avg_Daily_Spread": avg_daily_spread
        }
        for q in ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']:
            row[f"Disch_{q}"] = disch_shares[q]
            row[f"Charge_{q}"] = charge_shares[q]
        monthly_data.append(row)
        
    res_df = pd.DataFrame(monthly_data)
    
    # Plot Stacked Area
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 9), sharex=True)
    months_str = res_df["Month"].tolist()
    
    disch_matrix = np.array([res_df[f"Disch_{q}"].values for q in ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']])
    charge_matrix = np.array([res_df[f"Charge_{q}"].values for q in ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']])
    
    disch_colors = ['#e0e0e0', '#fdbb84', '#fc8d59', '#e34a33', '#b30000']
    charge_colors = ['#08519c', '#3182bd', '#6baed6', '#9ecae1', '#e0e0e0']
    
    # Discharge plot
    ax1.stackplot(months_str, disch_matrix, labels=['Q1 (Cheapest)', 'Q2', 'Q3', 'Q4', 'Q5 (Most Expensive)'], colors=disch_colors, alpha=0.9)
    ax1.set_title(f"{duid} Monthly Discharge Energy Share by Price Quintile", fontweight='bold')
    ax1.set_ylabel("Share of Monthly Discharge")
    ax1.set_ylim(0, 1.0)
    ax1.legend(loc='lower left', bbox_to_anchor=(1.02, 0.2))
    
    # Average daily spread overlay text
    for i, m_str in enumerate(months_str):
        spread_val = res_df.loc[i, "Avg_Daily_Spread"]
        ax1.text(i, 0.95, f"${spread_val:.0f}", ha='center', va='top', fontsize=8, color='black', fontweight='semibold')
    ax1.text(0, 0.98, "Prices: Monthly Avg Daily Spread ($/MWh)", ha='left', va='top', fontsize=8.5, color='#333333', fontstyle='italic')
    
    # Charge plot
    ax2.stackplot(months_str, charge_matrix, labels=['Q1 (Cheapest)', 'Q2', 'Q3', 'Q4', 'Q5 (Most Expensive)'], colors=charge_colors, alpha=0.9)
    ax2.set_title(f"{duid} Monthly Charge Energy Share by Price Quintile", fontweight='bold')
    ax2.set_ylabel("Share of Monthly Charge")
    ax2.set_xlabel("Month")
    ax2.set_ylim(0, 1.0)
    handles, labels = ax2.get_legend_handles_labels()
    ax2.legend(handles[::-1], labels[::-1], loc='upper left', bbox_to_anchor=(1.02, 0.8))
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    plot_path = os.path.join(output_dir, f"{duid.lower()}_quintile_share.png")
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved stacked area plot to {plot_path}")

def build_regression_dataset(df):
    daily_stats = df.groupby('DATE').agg({
        'CHARGE_ENERGY': 'sum',
        'DAILY_SPREAD': 'first'
    }).copy()
    
    q_charge = df[df['QUINTILE'] == 'Q1'].groupby('DATE')['CHARGE_ENERGY'].sum()
    daily_stats['CHARGE_Q1'] = q_charge
    daily_stats['CHARGE_Q1_SHARE'] = daily_stats['CHARGE_Q1'] / daily_stats['CHARGE_ENERGY']
    
    # Filter for low charging energy noise
    daily_stats = daily_stats[daily_stats['CHARGE_ENERGY'] >= 5.0].copy()
    
    start_date = daily_stats.index.min()
    daily_stats['DAYS_SINCE_START'] = (daily_stats.index - start_date).days
    
    bins = [0, 50, 150, 300, 99999]
    labels = ['Spread_0_50', 'Spread_50_150', 'Spread_150_300', 'Spread_300_plus']
    daily_stats['SPREAD_BIN'] = pd.cut(daily_stats['DAILY_SPREAD'], bins=bins, labels=labels)
    
    return daily_stats

def generate_regression_plot(hpr_daily, vbb_daily):
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Layout mapping: (row, col)
    # HPR1 Spread_150_300
    # HPR1 Spread_50_150
    # VBB1 Spread_50_150
    # VBB1 Spread_150_300
    
    configs = [
        {"df": hpr_daily, "duid": "HPR1", "bin": "Spread_150_300", "ax": axes[0, 0], "color": "#08519c", "line_color": "#b30000"},
        {"df": hpr_daily, "duid": "HPR1", "bin": "Spread_50_150", "ax": axes[0, 1], "color": "#3182bd", "line_color": "#737373"},
        {"df": vbb_daily, "duid": "VBB1", "bin": "Spread_50_150", "ax": axes[1, 0], "color": "#3182bd", "line_color": "#737373"},
        {"df": vbb_daily, "duid": "VBB1", "bin": "Spread_150_300", "ax": axes[1, 1], "color": "#08519c", "line_color": "#737373"}
    ]
    
    for cfg in configs:
        ax = cfg["ax"]
        bin_df = cfg["df"][cfg["df"]['SPREAD_BIN'] == cfg["bin"]].dropna(subset=['CHARGE_Q1_SHARE'])
        
        n = len(bin_df)
        x = bin_df['DAYS_SINCE_START']
        y = bin_df['CHARGE_Q1_SHARE']
        
        # Plot Scatter
        ax.scatter(x, y, color=cfg["color"], alpha=0.5, edgecolor='none', label="Daily Data")
        
        if n >= 10:
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            slope_per_month = slope * 30.4
            
            # Plot Regression Line
            x_range = np.linspace(x.min(), x.max(), 100)
            y_pred = intercept + slope * x_range
            ax.plot(x_range, y_pred, color=cfg["line_color"], linewidth=2.5, label="OLS Regression Fit")
            
            sig_text = "SIGNIFICANT" if p_value < 0.05 else "NOT SIGNIFICANT"
            p_text = f"p < 10⁻⁶" if p_value < 1e-6 else f"p = {p_value:.4f}"
            
            stat_label = (
                f"Slope: {slope_per_month*100:+.2f} pp/mo\n"
                f"R²: {r_value**2:.4f}\n"
                f"{p_text} ({sig_text})"
            )
            
            # Place text box in the upper-left or lower-right corner
            bbox_props = dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.9)
            ax.text(0.05, 0.95, stat_label, transform=ax.transAxes, fontsize=9.5, fontweight='bold' if p_value < 0.05 else 'normal',
                    verticalalignment='top', bbox=bbox_props)
        else:
            ax.text(0.5, 0.5, f"Insufficient Data (n={n})", transform=ax.transAxes, ha='center', va='center', fontsize=12)
            
        ax.set_title(f"{cfg['duid']} Charging Q1 Share: {cfg['bin']} (n={n})", fontweight='bold')
        ax.set_ylabel("Q1 Charge Energy Share")
        ax.set_xlabel("Days since 1 June 2025")
        ax.set_ylim(0, 1.0)
        ax.legend(loc='lower left')
        
    plt.tight_layout()
    reg_path = os.path.join(output_dir, "arbitrage_regression_test.png")
    plt.savefig(reg_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved OLS regression panel plot to {reg_path}")

if __name__ == "__main__":
    hpr_df = load_and_preprocess("HPR1", "SA1")
    vbb_df = load_and_preprocess("VBB1", "VIC1")
    
    # 1. Generate monthly stacked area plots
    generate_monthly_plots(hpr_df, "HPR1")
    generate_monthly_plots(vbb_df, "VBB1")
    
    # 2. Build regression datasets
    hpr_daily = build_regression_dataset(hpr_df)
    vbb_daily = build_regression_dataset(vbb_df)
    
    # 3. Generate 2x2 regression panels
    generate_regression_plot(hpr_daily, vbb_daily)
