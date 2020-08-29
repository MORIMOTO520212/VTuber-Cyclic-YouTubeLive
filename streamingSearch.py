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
import json

print("ライブ配信サーチ\n5分ごとに更新します。終了するにはCtril + Cを押してください。\n\n")

# ヘッドレスモードでユーザープロファイルを使う 
PROFILE_PATH = "C:\\Users\\kante\\AppData\\Local\\Google\\Chrome\\User Data"
options = Options()
# ヘッドレスではプロファイル情報を読み込まない
#options.add_argument("--headless")
#options.add_argument("--remote-debugging-port=9222")
options.add_argument('--user-data-dir=' + PROFILE_PATH)
driver = webdriver.Chrome(chrome_options=options)

while True:

    streamingChannels = []
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
            
            try:
                streamingNow = detail.find_all("span", class_=["ytd-badge-supported-renderer"])
                streamingNow = streamingNow[len(streamingNow)-1].get_text() # ライブ配信中
            except:
                streamingNow = False # 取得できなかった場合

            if streamingNow == "ライブ配信中":
                streamingChannels.append(channelId)
        
        with open("assets/streaming.json", "w") as f:
            json.dump(streamingChannels, f, indent=4)
        
        sleep(180) # 3分間待機

    except KeyboardInterrupt:
        print("キーが押されたので終了します。")
        driver.quit()
