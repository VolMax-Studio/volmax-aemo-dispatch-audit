import requests
from bs4 import BeautifulSoup

def scan_fpp_archives():
    folders = [
        "https://nemweb.com.au/Reports/ARCHIVE/FPPRATES/",
        "https://nemweb.com.au/Reports/ARCHIVE/FPPRUN/"
    ]
    for url in folders:
        print(f"\nScanning: {url}")
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                links = soup.find_all('a')
                filenames = []
                for l in links:
                    href = l.get('href')
                    if href and not href.startswith("?") and not href.startswith("/"):
                        filenames.append(href)
                print(f"Found {len(filenames)} files. Sample files:")
                for f in sorted(list(set(filenames)))[:10]:
                    print(f" - {f}")
            else:
                print(f"Failed, status code: {r.status_code}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    scan_fpp_archives()
