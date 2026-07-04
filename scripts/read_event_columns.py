import requests
import zipfile
import io
import pandas as pd

def read_cols():
    url = "https://nemweb.com.au/Reports/ARCHIVE/Causer_Pays_Scada/PUBLIC_CAUSER_PAYS_SCADA_20250818.zip"
    print(f"Downloading: {url}")
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        z = zipfile.ZipFile(io.BytesIO(r.content))
        matching = [name for name in z.namelist() if "20250819" in name]
        print(f"Found {len(matching)} files for August 19. Listing them:")
        for m in sorted(matching):
            print(f" - {m}")
        
        # Choose a file around 12:00 (e.g. 11:30 to 12:30)
        # Let's inspect the first file in the list to check the CSV structure
        if matching:
            target_file = sorted(matching)[0]
            print(f"\nInspecting CSV inside: {target_file}")
            nested_zip_data = z.read(target_file)
            nz = zipfile.ZipFile(io.BytesIO(nested_zip_data))
            csv_name = nz.namelist()[0]
            print(f"Found CSV: {csv_name}")
            csv_data = nz.read(csv_name)
            
            lines = csv_data.decode('utf-8').split('\n')
            print("First 20 lines of CSV:")
            for l in lines[:20]:
                print(l)
    else:
        print(f"Failed to access, status: {r.status_code}")

if __name__ == '__main__':
    read_cols()
