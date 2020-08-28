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
from time import sleep

# ヘッドレスモードでユーザープロファイルを使う 
PROFILE_PATH = "C:\\Users\\kante\\AppData\\Local\\Google\\Chrome\\User Data"
options = Options()
# ヘッドレスではプロファイル情報を読み込まない
#options.add_argument("--headless")
#options.add_argument("--remote-debugging-port=9222")
options.add_argument('--user-data-dir=' + PROFILE_PATH)
driver = webdriver.Chrome(chrome_options=options)

print("ライブ配信サーチ\n\n5分ごとに更新します。終了するにはCtril + Cを押してください。")
while True:
    try:
        driver.get("https://www.youtube.com/feed/subscriptions")
        source = driver.page_source

        soup = BeautifulSoup(source, 'html.parser')
        details = soup.find_all("div", id="details")
        print(len(details))
        for detail in details:
            channelLink = detail.find("a", class_=["yt-simple-endpoint style-scope", "yt-formatted-string"]).get("href")
            channelId = channelLink.replace("/channel/", "")
            # document.querySelectorAll("#details")[0].getElementsByTagName("span")[2].innerText;
            print(channelId)
            streamingNow = detail.find("span").get_text() # ~人が視聴中
            print(streamingNow)
        
        sleep(180)
    except KeyboardInterrupt:
        print("キーが押されたので終了します。")
        driver.quit()
