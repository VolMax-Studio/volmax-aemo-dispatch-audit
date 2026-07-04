import os
import zipfile
import io
import requests
import pandas as pd
import numpy as np

# Test list of URLs (limit to 2-3 files first to test, then run all)
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
os.makedirs(cache_dir, exist_ok=True)

def download_and_extract_freq(filename):
    url = f"https://nemweb.com.au/Reports/ARCHIVE/Causer_Pays_Scada/{filename}"
    cache_path = os.path.join(cache_dir, filename)
    
    if not os.path.exists(cache_path):
        print(f"Downloading {filename}...")
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            with open(cache_path, 'wb') as f:
                f.write(r.content)
        else:
            print(f"Failed to download {filename}: {r.status_code}")
            return pd.DataFrame()
            
    print(f"Extracting {filename}...")
    freq_records = []
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
                            
    df = pd.DataFrame(freq_records, columns=['time', 'deviation'])
    df['datetime'] = pd.to_datetime(df['time'], format='%Y/%m/%d %H:%M:%S')
    df = df.sort_values(by='datetime').drop_duplicates(subset=['datetime'])
    return df

print("Running test download and extract for one file...")
df_test = download_and_extract_freq(fcas_archive_files[0])
print(f"Extracted shape: {df_test.shape}")
if not df_test.empty:
    print(df_test.head())
