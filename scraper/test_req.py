import requests
from bs4 import BeautifulSoup

url = "https://www.furlenco.com/rent/products/sara-solid-wood-queen-bed-in-timeless-teak-finish-4730-rent"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
try:
    r = requests.get(url, headers=headers, timeout=10)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        print(f"Title Tag: {soup.title.text if soup.title else 'No Title'}")
        h1 = soup.find('h1')
        print(f"H1: {h1.text.strip() if h1 else 'No H1'}")
        
        # Check text length
        print(f"Text len: {len(r.text)}")
except Exception as e:
    print(f"Error: {e}")
