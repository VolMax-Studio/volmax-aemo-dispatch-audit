import requests
from bs4 import BeautifulSoup

def scan_archive():
    url = "https://nemweb.com.au/Reports/CURRENT/Dispatch_SCADA/"
    print(f"Scanning: {url}")
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            links = soup.find_all('a')
            folders = []
            for l in links:
                href = l.get('href')
                if href:
                    folders.append(href)
            print("Found folders/links:")
            for f in sorted(list(set(folders))):
                print(f" - {f}")
        else:
            print(f"Directory not accessible, status code: {r.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    scan_archive()
