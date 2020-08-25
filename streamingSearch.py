# チャンネルリンクを取得する。
# document.querySelectorAll("#details")[インデックス番号].querySelector("#text > a").href;
# "https://www.youtube.com/channel/UCoztvTULBYd3WmStqYeoHcA"

# 配信中かどうかを調べる。
# 100件取得できるので0~99まで回す。取得順序はランダムである。
# document.querySelectorAll("#details")[0].getElementsByTagName("span")[2].innerText;
# "ライブ配信中"

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# ユーザープロファイルを使う
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=options)
driver.get("http://free-proxy.cz/ja/proxylist/main/1")
source = driver.page_source
driver.quit()

soup = BeautifulSoup(res.text, 'html.parser')


details = soup.find_all("div", id="details")

print(details)