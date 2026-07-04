import os
import zipfile
import io
import pandas as pd

filename = "PUBLIC_CAUSER_PAYS_SCADA_20250818.zip"
cache_path = os.path.join("./data/raw_cache", filename)

print(f"Checking datetimes in {filename}...")
freq_records = []
with zipfile.ZipFile(cache_path, 'r') as z:
    for name in sorted(z.namelist())[:5]: # just check first few nested zip files
        if not name.endswith('.zip'):
            continue
        nested_zip_data = z.read(name)
        with zipfile.ZipFile(io.BytesIO(nested_zip_data), 'r') as nz:
            for csv_name in nz.namelist():
                csv_data = nz.read(csv_name)
                lines = csv_data.decode('utf-8').split('\n')
                for line in lines[:200]: # first few lines
                    parts = line.strip().split(',')
                    if len(parts) >= 8 and parts[0] == 'D' and parts[2] == 'NETWORK' and parts[5] == 'MAINLAND':
                        meas_time_str = parts[4].replace('"', '').strip()
                        freq_dev = float(parts[6])
                        freq_records.append((meas_time_str, freq_dev))
                        
df = pd.DataFrame(freq_records, columns=['time', 'deviation'])
df['datetime'] = pd.to_datetime(df['time'], format='%Y/%m/%d %H:%M:%S')
print(f"Min datetime: {df['datetime'].min()}")
print(f"Max datetime: {df['datetime'].max()}")
