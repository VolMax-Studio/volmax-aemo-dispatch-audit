import requests
import json

urls = [
    "https://nemweb.com.au/Reports/ARCHIVE/Causer_Pays_Scada/PUBLIC_CAUSER_PAYS_SCADA_20250601.zip",
    "https://nemweb.com.au/Reports/ARCHIVE/Causer_Pays_Scada/PUBLIC_CAUSER_PAYS_SCADA_20250608.zip",
    "https://nemweb.com.au/Reports/ARCHIVE/Causer_Pays_Scada/PUBLIC_CAUSER_PAYS_SCADA_20250615.zip"
]

for url in urls:
    api_url = f"https://web.archive.org/cdx/search/cdx?url={url}&output=json"
    print(f"Checking Wayback Machine for: {url}")
    try:
        r = requests.get(api_url, timeout=15)
        if r.status_code == 200:
            data = r.json()
            if len(data) > 1:
                print(f"  -> Found {len(data) - 1} snapshot(s)!")
                print(f"  -> Details: {data[1:]}")
            else:
                print("  -> No snapshots found (empty CDX response).")
        else:
            print(f"  -> API returned status code: {r.status_code}")
    except Exception as e:
        print(f"  -> Error querying Wayback: {e}")
