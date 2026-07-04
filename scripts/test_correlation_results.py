import os
import json
import glob
import pandas as pd
import numpy as np

def main():
    print("======================================================================")
    print("ANALYZING CORRELATION BETWEEN BESS DEVIATION AND GRID FREQUENCY VOLATILITY")
    print("======================================================================")
    
    # Load L1 integrity report to get accepted BESS units
    l1_report_path = './data/processed/l1_integrity_report.json'
    with open(l1_report_path, 'r') as f:
        l1_report = json.load(f)
    
    # We will use the 17 accepted units
    accepted_units = l1_report.get("accepted", [])
    accepted_duids = [u["DUID"] for u in accepted_units]
    bess_info = {u["DUID"]: u["Capacity_MW"] for u in accepted_units}
    
    # Load compiled 5-minute frequency data
    freq_df = pd.read_feather('./data/processed/fcas_frequency_5min.feather')
    print(f"Loaded {len(freq_df)} frequency intervals.")
    
    # Stitch processed monthly SCADA and dispatch files for Jun-Sept 2025
    proc_dir = './data/processed'
    months = ['202506', '202507', '202508', '202509']
    
    scada_list = []
    dispatch_list = []
    for m in months:
        sf = os.path.join(proc_dir, f"scada_{m}.feather")
        df_file = os.path.join(proc_dir, f"dispatch_{m}.feather")
        if os.path.exists(sf) and os.path.exists(df_file):
            scada_list.append(pd.read_feather(sf))
            dispatch_list.append(pd.read_feather(df_file))
            
    scada_df = pd.concat(scada_list, ignore_index=True)
    dispatch_df = pd.concat(dispatch_list, ignore_index=True)
    
    # Filter for accepted units
    scada_df = scada_df[scada_df['DUID'].isin(accepted_duids)]
    dispatch_df = dispatch_df[dispatch_df['DUID'].isin(accepted_duids)]
    
    results = []
    
    for duid in accepted_duids:
        cap = bess_info[duid]
        conformance_band = max(6.0, 0.03 * cap)
        
        s_sub = scada_df[scada_df['DUID'] == duid].copy()
        d_sub = dispatch_df[dispatch_df['DUID'] == duid].copy()
        
        if s_sub.empty or d_sub.empty:
            continue
            
        # Shift dispatch targets forward by 5 minutes: MATCH_DATE = SETTLEMENTDATE + 5 minutes
        d_sub['MATCH_DATE'] = d_sub['SETTLEMENTDATE'] + pd.Timedelta(minutes=5)
        
        # Merge target TOTALCLEARED(t) with actual SCADAVALUE(t+5)
        merged = pd.merge(
            d_sub[['MATCH_DATE', 'TOTALCLEARED']],
            s_sub[['SETTLEMENTDATE', 'SCADAVALUE']],
            left_on='MATCH_DATE',
            right_on='SETTLEMENTDATE',
            how='inner'
        )
        
        if merged.empty:
            continue
            
        merged['DEVIATION'] = merged['SCADAVALUE'] - merged['TOTALCLEARED']
        merged['ABS_DEVIATION'] = merged['DEVIATION'].abs()
        merged['EXCEEDANCE'] = merged['ABS_DEVIATION'] > conformance_band
        
        # Merge with frequency data
        merged_freq = pd.merge(
            merged,
            freq_df,
            left_on='SETTLEMENTDATE',
            right_on='datetime',
            how='inner'
        )
        
        if merged_freq.empty:
            continue
            
        # Drop rows with NaN frequency std
        merged_freq = merged_freq.dropna(subset=['freq_std'])
        
        if len(merged_freq) < 100:
            continue
            
        # Compute correlation
        corr_val = merged_freq['ABS_DEVIATION'].corr(merged_freq['freq_std'])
        
        # Compare volatility during exceedance vs normal intervals
        exc_df = merged_freq[merged_freq['EXCEEDANCE'] == True]
        norm_df = merged_freq[merged_freq['EXCEEDANCE'] == False]
        
        mean_std_exc = exc_df['freq_std'].mean()
        mean_std_norm = norm_df['freq_std'].mean()
        
        pct_diff = ((mean_std_exc - mean_std_norm) / mean_std_norm * 100.0) if mean_std_norm > 0 else 0.0
        
        # Excursion rate comparison
        excursion_exc = exc_df['freq_excursion_pct'].mean()
        excursion_norm = norm_df['freq_excursion_pct'].mean()
        
        results.append({
            "DUID": duid,
            "Capacity": cap,
            "Intervals": len(merged_freq),
            "Exceedances": len(exc_df),
            "Correlation": corr_val,
            "Mean_Std_Exceedance": mean_std_exc,
            "Mean_Std_Normal": mean_std_norm,
            "Pct_Diff": pct_diff,
            "Excursion_Rate_Exceedance": excursion_exc,
            "Excursion_Rate_Normal": excursion_norm
        })
        
    res_df = pd.DataFrame(results).sort_values(by='Correlation', ascending=False)
    print(res_df.to_string(index=False))

if __name__ == '__main__':
    main()
