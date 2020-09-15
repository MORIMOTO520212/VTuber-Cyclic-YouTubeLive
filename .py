import requests
from bs4 import BeautifulSoup
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
res = requests.get("http://twttrend.com", headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')
print(soup)