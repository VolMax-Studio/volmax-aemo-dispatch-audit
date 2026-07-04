import requests
from bs4 import BeautifulSoup

def check_nemweb():
    url = "https://nemweb.com.au/Reports/CURRENT/MMSDM/2026/"
    print(f"Scanning: {url}")
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            links = soup.find_all('a')
            folders = []
            for l in links:
                href = l.get('href')
                if href and 'MMSDM' in href:
                    folders.append(href.split('/')[-2])
            print("Found folders:")
            for f in sorted(list(set(folders))):
                print(f" - {f}")
                
            # Scan inside MMSDM_2026_06 if it exists
            june_folder = "MMSDM_2026_06"
            if june_folder in folders:
                june_url = f"{url}{june_folder}/"
                print(f"\nScanning June folder: {june_url}")
                jr = requests.get(june_url, timeout=10)
                if jr.status_code == 200:
                    jsoup = BeautifulSoup(jr.text, 'html.parser')
                    jlinks = jsoup.find_all('a')
                    jfiles = []
                    for jl in jlinks:
                        jh = jl.get('href')
                        if jh and ('DISPATCH' in jh or 'dispatch' in jh):
                            jfiles.append(jh.split('/')[-1])
                    print(f"Found {len(jfiles)} dispatch files in June folder.")
                    for jf in sorted(jfiles)[:10]:
                        print(f" - {jf}")
        else:
            print(f"Directory not accessible, status code: {r.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    check_nemweb()
