import requests
import zipfile
import io
import os

def download_and_list():
    url = "https://nemweb.com.au/Reports/ARCHIVE/Causer_Pays_Scada/PUBLIC_CAUSER_PAYS_SCADA_20250825.zip"
    print(f"Downloading: {url}")
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        z = zipfile.ZipFile(io.BytesIO(r.content))
        print("Internal files in the zip:")
        for name in z.namelist():
            print(f" - {name}")
    else:
        print(f"Failed to download, status: {r.status_code}")

if __name__ == '__main__':
    download_and_list()
