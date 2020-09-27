from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import json, requests, tweepy


print("ライブ配信サーチ\n5分ごとに更新します。終了するにはCtril + Cを押してください。\n\n")

with open("setting.json", "r") as f:
    setting = json.load(f)

consumer_key='fOr1fbI9mCK1ztiqbEIMlHfLV'
consumer_secret='PdVL9Fb166jY7VMjXuA8EkjN4mWNlkEFI6XT3mTIEbqkVDGwMb'
access_key='4634604300-uYOEizJIhTQWMan2pLtfK9r73nXK5BK0h4rlwf3'
access_secret='54Dqdt8Kx7CoVKq2XqOSoTsKkTI7liPtpPugaZjGrTbRK'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth_handler=auth)

# ヘッドレスモードでユーザープロファイルを使う 
# C:\\Users\\kante\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\so4o45dh.default
Options = webdriver.FirefoxOptions()
#Options.set_headless() Linuxでは非推奨
Options.headless = True
PROFILE_PATH = setting["firefoxProfilePath"]
Options.profile = PROFILE_PATH
Options.binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
driver = webdriver.Firefox(options=Options) # firefox_optionsはLinuxでは非推奨

while True:

    with open("database/streamdata.json", "r") as f:
        streamdata = json.load(f)

    streamingChannels = []
    try:
        driver.get("https://www.youtube.com/feed/subscriptions")
        source = driver.page_source

        soup = BeautifulSoup(source, 'html.parser')
        details = soup.find_all("div", id="details")
        print("取得チャンネル数："+str(len(details)))
        for detail in details:
            channelLink = detail.find("a", class_=["yt-simple-endpoint style-scope", "yt-formatted-string"]).get("href")
            channelId   = channelLink.replace("/channel/", "") # チャンネルID
            try:
                # [ライブ配信中]マークを抽出
                streamingNow    = detail.find_all("span", class_=["ytd-badge-supported-renderer"])
                streamingNow    = streamingNow[len(streamingNow)-1].get_text() # ライブ配信中

                # 視聴者数を抽出
                streamingNumber = detail.find_all("span", class_=["ytd-grid-video-renderer"])
                streamingNumber = streamingNumber[len(streamingNumber)-1].get_text() # 1.5万 人が視聴中
                streamingNumber = streamingNumber.replace(" 人が視聴中", "人") # 同時接続者数

                # 動画タイトルを抽出
                videoTitle = detail.find_all("a", id="video-title")[0].get("title")

            except Exception as e:
                streamingNow = False # 取得できなかった場合

            if streamingNow == "ライブ配信中":
                # 登録済か未登録か
                for channelIdData in streamdata.keys():
                    if channelIdData == channelId:
                        break
                else:
                    print("未登録のライバー："+channelId)
                    channelId = "unregistered"

                if channelId != "unregistered": # 登録済みユーザーのみ

                    if 200 == requests.get(streamdata[channelId]["photo"]).status_code: # アイコンのURLが有効である場合のみ
                        
                        streamingChannels.append({"channelId": channelId, "streamingNumber": streamingNumber, "videoTitle": videoTitle}) # ストリーミングに追加
                    else:
                        # tweepyを使ってアイコン更新
                        with open("database/streamdata.json", "r") as f:
                            streamdata = json.load(f)
                            
                        try:
                            userStatus = api.get_user(streamdata[channelId]["twitterId"])
                            photo = userStatus.profile_image_url_https
                        except Exception as e:
                            if "User not found" in str(e): # Twitterアカウントが見つからなかった場合
                                print(streamdata[channelId]["userName"]+"さんのTwitterのアカウントが見つかりませんでした。")
                                continue

                        streamdata[channelId]["photo"] = photo.replace("_normal.jpg", "_400x400.jpg").replace("_normal.png", "_400x400.png")
                        # 書き込み
                        print(streamdata[channelId]["userName"]+"さんのアイコンデータを更新しました。")
                        with open("database/streamdata.json", "w") as f:
                            json.dump(streamdata, f, indent=4)

        if streamingChannels == []: # ライブ配信を誰もしていない場合は今後の予定を記録する
            print("ライブ配信者なし")
        else:
            print("配信者数："+str(len(streamingChannels)))

        with open("assets/streaming.json", "w") as f:
            json.dump(streamingChannels, f, indent=4)
        
        sleep(180) # 3分間待機

    except KeyboardInterrupt:
        print("キーが押されたので終了します。")
        driver.quit()
        exit()

    except Exception as e:
        if "HTTPSConnectionPool" in str(e) or "NewConnectionError" in str(e):
            print("ネットの接続が不安定です。")
        else:
            print("エラー",str(e))