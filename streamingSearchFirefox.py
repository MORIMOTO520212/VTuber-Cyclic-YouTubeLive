from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import sys, json, requests, tweepy, settings, datetime


print("ライブ配信サーチ\n5分ごとに更新します。終了するにはCtril + Cを押してください。")


# 動作環境の設定 windows | linux
os = "windows"

print("動作オペレーティングシステム："+os)

consumer_key, consumer_secret, access_key, access_secret = settings.tweepyKeyPath()

print("tweepy API...")
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth_handler=auth)

print("selenium webdriver...")
# ヘッドレスモードでユーザープロファイルを使う
Options = webdriver.FirefoxOptions()
Options.headless = True #Options.set_headless() Linuxでは非推奨
PROFILE_PATH = settings.firefoxProfilePath(os)
Options.profile = PROFILE_PATH
driver = webdriver.Firefox(options=Options) # firefox_optionsはLinuxでは非推奨

with open(settings.idChangeDataPath(os), "r") as f:
    idChangeData = json.load(f)
with open(settings.streamDataPath(os), "r") as f:
    streamdata = json.load(f)
with open(settings.gamesDataPath(os), "r") as f:
    gamesData = json.load(f)

streamingChannels_before = {}
print("complete!")


def getSource():
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
    return details

def search(detail):
    # Channel IDの取得
    streamingNumber = ""
    videoTitle = ""

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

    except:
        streamingNow = False

    return channelId, streamingNow, streamingNumber, videoTitle

def updateTwitterIcon(channelId):
    usrRoot = streamdata[channelId]
    try:
        userStatus = api.get_user(usrRoot["twitterId"])
        photo = userStatus.profile_image_url_https
        usrRoot["photo"] = photo.replace("_normal.jpg", "_400x400.jpg").replace("_normal.png", "_400x400.png")
        usrRoot["iconUpdateCount"] += 1
        print(usrRoot["userName"]+"さんのアイコンデータを更新しました。")
    except Exception as e:
        if "User not found" in str(e): # Twitterアカウントが見つからなかった場合
            print(usrRoot["userName"]+"さんのTwitterのアカウントが見つかりませんでした。 "+channelId)

def sort(play):
    # streamingDataのデータを比較すると古いデータと比較しているし、更新されていないので完璧な処理が出来ていない。
    # 最初の１～３くらいまでは正確に処理できる確立が高いが、古いデータを参照するので、時間がたつと、既存データの書き写し処理の意味がなくなってします。
    for strDa in streamingChannels_before:
        # 既存のデータが新規のデータに含まれていた場合そのまま書き写す
        if strDa["channelId"] in str(streamingChannels):

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
                "livePointStatus" : strDa["livePointStatus"],
                "play": strDa["play"]
            })

    for strCha in streamingChannels:
        if strCha["channelId"] not in str(streamingChannels_before): # 書き込み用データにまだ含まれていない場合末尾に書く

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
                "livePointStatus" : strCha["livePointStatus"],
                "play": strCha["play"]
            })

def playGame(videoTitle):
    game = {}

    videoTitle = str.upper(videoTitle) # アルファベット大文字変換
    videoTitle = videoTitle.replace(" ", "")

    for gameData in gamesData:
        for productName in gameData["word"].split(";"):
            if productName in videoTitle:
                game["product"] = gameData["product"]
                game["url"]     = gameData["url"]
                game["photo"]   = gameData["photo"]
                break
        else:
            continue
        break
    else:
        return False

    return game

def updateStatus(usrRoot, play):
    now = datetime.datetime.now()
    # ライブポイント
    usrRoot["livePoint"] += 1
    # 最終ライブ日
    usrRoot["lastLiveDate"] = now.strftime("%Y/%m/%d %H:%M:%S")
    # アクティブ
    hour = str(now.hour)
    if len(hour) == 1: hour = "0"+hour
    usrRoot["livePointStatus"][hour] += 1
    # 最終アイコンアップデート日
    usrRoot["lastIconUpdateDate"] = now.strftime("%Y/%m/%d %H:%M:%S")
    # プレイしたゲーム
    if play:
        # プレイ中のゲームが記録されていなければ新しく追加する
        for game in usrRoot["games"]:
            if play["product"] == game["product"]:
                break
        else:
            usrRoot["games"].append(play)


while True:
    try:
        streamingChannels = []
        streamingDataNew  = [] # 書き込み用

        # YouTubeからデータを取得
        details = getSource()
        
        # スクレイピング
        for detail in details:
            channelId, streamingNow, streamingNumber, videoTitle = search(detail)

            if streamingNow == "ライブ配信中" or streamingNow == "LIVE NOW":
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
                    
                    usrRoot = streamdata[channelId]

                    # タイトルにゲーム名がある場合取得
                    play = playGame(videoTitle)

                    # アイコンのリンクが切れていないか確認し、tweepyを使ってアイコン更新
                    if 200 != requests.get(usrRoot["photo"]).status_code:
                        updateTwitterIcon(channelId)

                    streamingChannels.append({ # ストリーミングに追加
                        "channelId": channelId,
                        "userName": usrRoot["userName"],
                        "twitterId": usrRoot["twitterId"],
                        "streamingNumber": streamingNumber,
                        "videoTitle": videoTitle,
                        "photo": usrRoot["photo"],
                        "livePoint": usrRoot["livePoint"],
                        "lastLiveDate": usrRoot["lastLiveDate"],
                        "iconUpdateCount": usrRoot["iconUpdateCount"],
                        "lastIconUpdateDate": usrRoot["lastIconUpdateDate"],
                        "livePointStatus" : usrRoot["livePointStatus"],
                        "play": play
                    })

                    # ライバーステータス更新
                    updateStatus(usrRoot, play)


        if streamingChannels == []: # （未完成）ライブ配信を誰もしていない場合は今後の予定を記録する
            pass
        else:
            # チャンネルデータのソート　新しいデータは末尾に追加する
            sort(play)

        print("取得チャンネル数：{}　配信者数：{}".format(str(len(details)), str(len(streamingChannels))))

        # 書き込み
        with open(settings.streamingDataPath(os), "w") as f:
            json.dump(streamingDataNew, f)

        with open(settings.streamDataPath(os), "w") as f:
            json.dump(streamdata, f, indent=4)

        # データを保持　次のクロール時にデータを比較するため
        streamingChannels_before = streamingChannels

        # 3分間待機
        sleep(180)
    
    except KeyboardInterrupt:
        print("キーが押されたので終了します。")
        driver.quit()
        sys.exit()