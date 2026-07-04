import requests
from bs4 import BeautifulSoup

def check_nemweb():
    url = "https://nemweb.com.au/Reports/ARCHIVE/Causer_Pays_Scada/"
    print(f"Scanning: {url}")
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            links = soup.find_all('a')
            filenames = []
            for l in links:
                href = l.get('href')
                if href and ('PUBLIC' in href or '.zip' in href):
                    # Clean href (remove path prefix if any)
                    clean_name = href.split('/')[-1]
                    filenames.append(clean_name)
            
            print(f"Found {len(filenames)} files:")
            for f in sorted(filenames):
                print(f" - {f}")
        else:
            print(f"Directory not accessible, status code: {r.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    check_nemweb()
