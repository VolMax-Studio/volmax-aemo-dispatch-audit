import requests
import zipfile
import io

def locate_event():
    urls = [
        "https://nemweb.com.au/Reports/ARCHIVE/Causer_Pays_Scada/PUBLIC_CAUSER_PAYS_SCADA_20250818.zip",
        "https://nemweb.com.au/Reports/ARCHIVE/Causer_Pays_Scada/PUBLIC_CAUSER_PAYS_SCADA_20250825.zip",
    ]
    for url in urls:
        print(f"\nChecking: {url}")
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            z = zipfile.ZipFile(io.BytesIO(r.content))
            namelist = z.namelist()
            matching_files = [n for n in namelist if "20250819" in n]
            print(f"Total files in zip: {len(namelist)}")
            print(f"Files matching '20250819': {len(matching_files)}")
            if matching_files:
                print("First 5 matching files:")
                for mf in matching_files[:5]:
                    print(f"  - {mf}")
        else:
            print(f"Failed to access {url}, status: {r.status_code}")

if __name__ == '__main__':
    locate_event()
