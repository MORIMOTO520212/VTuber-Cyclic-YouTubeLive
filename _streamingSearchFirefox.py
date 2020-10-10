from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import json, requests, tweepy, settings, datetime


print("ライブ配信サーチ\n5分ごとに更新します。終了するにはCtril + Cを押してください。")


# 動作環境の設定 windows | linux
os = "linux"

print("動作オペレーティングシステム："+os)

consumer_key='fOr1fbI9mCK1ztiqbEIMlHfLV'
consumer_secret='PdVL9Fb166jY7VMjXuA8EkjN4mWNlkEFI6XT3mTIEbqkVDGwMb'
access_key='4634604300-uYOEizJIhTQWMan2pLtfK9r73nXK5BK0h4rlwf3'
access_secret='54Dqdt8Kx7CoVKq2XqOSoTsKkTI7liPtpPugaZjGrTbRK'

print("tweepy API...")
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth_handler=auth)

print("selenium webdriver...")
# ヘッドレスモードでユーザープロファイルを使う 
# C:\\Users\\kante\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\so4o45dh.default
Options = webdriver.FirefoxOptions()
#Options.set_headless() Linuxでは非推奨
Options.headless = True
PROFILE_PATH = settings.firefoxProfilePath(os)
Options.profile = PROFILE_PATH
#Options.binary_location = settings.firefoxBinaryPath() windows
driver = webdriver.Firefox(options=Options) # firefox_optionsはLinuxでは非推奨

with open(settings.idChangeDataPath(os), "r") as f:
    idChangeData = json.load(f)

print("complete!")
while True:

    with open(settings.streamDataPath(os), "r") as f:
        streamdata = json.load(f)
    
    with open(settings.streamingDataPath(os), "r") as f:
        streamingData = json.load(f)

    streamingChannels = []
    try:
        driver.get("https://www.youtube.com/feed/subscriptions")

        # 2つ目のチャンネルブロックを取得するために最下部までスクロール
        driver.execute_script("window.scrollTo(0, 5000);")
        soup = ""
        for _ in range(5): # スクロールの検出とソースの取得　タイムアウト時間最大50秒
            sleep(10)
            source = driver.page_source
            soup = BeautifulSoup(source, 'html.parser')
            channelbrock = soup.find_all("ytd-item-section-renderer", class_=["style-scope", "ytd-section-list-renderer"])
            if 2 == len(channelbrock):
                break
            else:
                print("再試行{}：2つのチャンネルブロックのロードが完了しませんでした。".format(str(_+1)))
                driver.execute_script("window.scrollTo(0, 1000);")

        details = soup.find_all("div", id="details")

        # Channel IDの取得
        for detail in details:
            channelLink = detail.find("a", class_=["yt-simple-endpoint style-scope", "yt-formatted-string"]).get("href")
            channelId   = channelLink.replace("/channel/", "")
            try:
                # [ライブ配信中]マークを抽出
                streamingNow    = detail.find_all("span", class_=["ytd-badge-supported-renderer"])
                streamingNow    = streamingNow[len(streamingNow)-1].get_text()

                # 視聴者数を抽出
                streamingNumber = detail.find_all("span", class_=["ytd-grid-video-renderer"])
                streamingNumber = streamingNumber[len(streamingNumber)-1].get_text()
                streamingNumber = streamingNumber.replace(" 人が視聴中", "人")

                # 動画タイトルを抽出
                videoTitle = detail.find_all("a", id="video-title")[0].get("title")

            except Exception as e:
                streamingNow = False

            if streamingNow == "ライブ配信中":
                # 登録済か未登録か
                for channelIdData in streamdata.keys():
                    if channelIdData == channelId:
                        break
                else:
                    try: # ユーザー名でチャンネルIDが取得された場合
                        channelId = idChangeData[channelId]

                    except:
                        print("未登録のライバー："+channelId)
                        channelId = "unregistered"

                if channelId != "unregistered": # 登録済みユーザーのみ

                    if 200 == requests.get(streamdata[channelId]["photo"]).status_code: # アイコンのURLが有効である場合のみ
                        
                        streamingChannels.append({ # ストリーミングに追加
                            "channelId": channelId,
                            "userName": streamdata[channelId]["userName"],
                            "twitterId": streamdata[channelId]["twitterId"],
                            "streamingNumber": streamingNumber,
                            "videoTitle": videoTitle,
                            "photo": streamdata[channelId]["photo"],
                            "livePoint": streamdata[channelId]["livePoint"],
                            "lastLiveDate": streamdata[channelId]["lastLiveDate"],
                            "iconUpdateCount": streamdata[channelId]["iconUpdateCount"],
                            "lastIconUpdateDate": streamdata[channelId]["lastIconUpdateDate"],
                            "livePointStatus" : streamdata[channelId]["livePointStatus"]
                        })

                    else:
                        # tweepyを使ってアイコン更新
                        try:
                            userStatus = api.get_user(streamdata[channelId]["twitterId"])
                            photo = userStatus.profile_image_url_https
                            streamdata[channelId]["photo"] = photo.replace("_normal.jpg", "_400x400.jpg").replace("_normal.png", "_400x400.png")
                            streamdata[channelId]["iconUpdateCount"] += 1
                            print(streamdata[channelId]["userName"]+"さんのアイコンデータを更新しました。")
                        except Exception as e:
                            if "User not found" in str(e): # Twitterアカウントが見つからなかった場合
                                print(streamdata[channelId]["userName"]+"さんのTwitterのアカウントが見つかりませんでした。")

                    # ライバーステータス更新
                    now = datetime.datetime.now()
                    streamdata[channelId]["livePoint"] += 1
                    streamdata[channelId]["lastLiveDate"] = now.strftime("%Y/%m/%d %H:%M:%S")
                    hour = str(now.hour)
                    if len(hour) == 1: hour = "0"+hour
                    streamdata[channelId]["livePointStatus"][hour] += 1
                    streamdata[channelId]["lastIconUpdateDate"] = now.strftime("%Y/%m/%d %H:%M:%S")

        streamingDataNew = [] # 書き込み用

        if streamingChannels == []: # （未完成）ライブ配信を誰もしていない場合は今後の予定を記録する
            pass
        else:

            # チャンネルデータのソート　新しいデータは末尾に追加する
            for strDa in streamingData:
                if strDa["channelId"] in str(streamingChannels): # 既存のデータが新規のデータに含まれていた場合そのまま書き写す

                    streamingDataNew.append({ # 既存ライバー追加
                        "channelId": strDa["channelId"],
                        "userName": strDa["userName"],
                        "twitterId": strDa["twitterId"],
                        "streamingNumber": strDa["streamingNumber"],
                        "videoTitle": strDa["videoTitle"],
                        "photo": strDa["photo"],
                        "livePoint": strDa["livePoint"],
                        "lastLiveDate": strDa["lastLiveDate"],
                        "iconUpdateCount": strDa["iconUpdateCount"],
                        "lastIconUpdateDate": strDa["lastIconUpdateDate"],
                        "livePointStatus" : strDa["livePointStatus"]
                    })

            for strCha in streamingChannels:
                if strCha["channelId"] not in str(streamingData): # 書き込み用データにまだ含まれていない場合末尾に書く

                    streamingDataNew.append({ # 開始ライバー追加
                        "channelId": strCha["channelId"],
                        "userName": strCha["userName"],
                        "twitterId": strCha["twitterId"],
                        "streamingNumber": strCha["streamingNumber"],
                        "videoTitle": strCha["videoTitle"],
                        "photo": strCha["photo"],
                        "livePoint": strCha["livePoint"],
                        "lastLiveDate": strCha["lastLiveDate"],
                        "iconUpdateCount": strCha["iconUpdateCount"],
                        "lastIconUpdateDate": strCha["lastIconUpdateDate"],
                        "livePointStatus" : strCha["livePointStatus"]
                    })

        print("取得チャンネル数：{}　配信者数：{}".format(str(len(details)), str(len(streamingChannels))))

        # 書き込み
        with open(settings.streamingDataPath(os), "w") as f:
            json.dump(streamingDataNew, f)

        with open(settings.streamDataPath(os), "w") as f:
            json.dump(streamdata, f, indent=4)
        
        # 3分間待機
        sleep(180)

    except KeyboardInterrupt:
        print("キーが押されたので終了します。")
        driver.quit()
        exit()

    except Exception as e:
        if "HTTPSConnectionPool" in str(e) or "NewConnectionError" in str(e):
            print("ネットの接続が不安定です。")
        else:
            print("エラー：",str(e))