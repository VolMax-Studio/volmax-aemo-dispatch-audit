import os
import zipfile
import io
import requests
import pandas as pd
import numpy as np

def main():
    print("======================================================================")
    print("STARTING FCAS FREQUENCY TELEMETRY COMPILATION (June - September 2025)")
    print("======================================================================")
    
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
    
    cache_dir = "./data/raw_cache"
    proc_dir = "./data/processed"
    os.makedirs(cache_dir, exist_ok=True)
    os.makedirs(proc_dir, exist_ok=True)
    
    output_feather = os.path.join(proc_dir, "fcas_frequency_5min.feather")
    
    if os.path.exists(output_feather):
        print(f"Processed frequency data already exists at {output_feather}. Loading cached version.")
        df_all = pd.read_feather(output_feather)
        print(f"Loaded {len(df_all)} intervals from cache.")
        return df_all
        
    all_resampled = []
    
    for filename in fcas_archive_files:
        url = f"https://nemweb.com.au/Reports/ARCHIVE/Causer_Pays_Scada/{filename}"
        cache_path = os.path.join(cache_dir, filename)
        
        if not os.path.exists(cache_path):
            print(f"Downloading {filename}...")
            r = requests.get(url, timeout=30)
            if r.status_code == 200:
                with open(cache_path, 'wb') as f:
                    f.write(r.content)
            else:
                print(f"Warning: Failed to download {filename}, status: {r.status_code}")
                continue
                
        print(f"Extracting & processing frequency from {filename}...")
        freq_records = []
        try:
            with zipfile.ZipFile(cache_path, 'r') as z:
                for name in sorted(z.namelist()):
                    if not name.endswith('.zip'):
                        continue
                    nested_zip_data = z.read(name)
                    with zipfile.ZipFile(io.BytesIO(nested_zip_data), 'r') as nz:
                        for csv_name in nz.namelist():
                            csv_data = nz.read(csv_name)
                            lines = csv_data.decode('utf-8').split('\n')
                            for line in lines:
                                parts = line.strip().split(',')
                                if len(parts) >= 8 and parts[0] == 'D' and parts[2] == 'NETWORK' and parts[5] == 'MAINLAND':
                                    meas_time_str = parts[4].replace('"', '').strip()
                                    freq_dev = float(parts[6])
                                    freq_records.append((meas_time_str, freq_dev))
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue
            
        if not freq_records:
            continue
            
        df = pd.DataFrame(freq_records, columns=['time', 'deviation'])
        df['datetime'] = pd.to_datetime(df['time'], format='%Y/%m/%d %H:%M:%S')
        # Filter for 2025 to remove telemetry anomalies
        df = df[df['datetime'].dt.year == 2025]
        df = df.sort_values(by='datetime').drop_duplicates(subset=['datetime'])
        
        # Resample to 5-minute intervals (label='right', closed='right' to match dispatch targets)
        # We calculate the standard deviation and max absolute deviation
        resampled_std = df.resample('5min', on='datetime', label='right', closed='right')['deviation'].std().reset_index()
        resampled_std.rename(columns={'deviation': 'freq_std'}, inplace=True)
        
        resampled_max = df.resample('5min', on='datetime', label='right', closed='right')['deviation'].apply(lambda x: x.abs().max() if len(x) > 0 else np.nan).reset_index()
        resampled_max.rename(columns={'deviation': 'freq_max_dev'}, inplace=True)
        
        # Excursion percentage (where |dev| > 0.15 Hz)
        resampled_excursion = df.resample('5min', on='datetime', label='right', closed='right')['deviation'].apply(
            lambda x: (x.abs() > 0.15).mean() * 100.0 if len(x) > 0 else np.nan
        ).reset_index()
        resampled_excursion.rename(columns={'deviation': 'freq_excursion_pct'}, inplace=True)
        
        merged_resampled = pd.merge(resampled_std, resampled_max, on='datetime')
        merged_resampled = pd.merge(merged_resampled, resampled_excursion, on='datetime')
        
        all_resampled.append(merged_resampled)
        print(f"  Processed {len(merged_resampled)} 5-minute intervals.")
        
    if not all_resampled:
        print("Error: No frequency data was processed.")
        return pd.DataFrame()
        
    df_all = pd.concat(all_resampled, ignore_index=True)
    df_all = df_all.sort_values(by='datetime').drop_duplicates(subset=['datetime'])
    
    # Save to feather
    df_all.to_feather(output_feather)
    print(f"\nSaved {len(df_all)} intervals to {output_feather}")
    return df_all

if __name__ == '__main__':
    main()
