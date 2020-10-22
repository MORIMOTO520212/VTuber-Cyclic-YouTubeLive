from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import sys, json, requests, tweepy, settings, datetime


print("ライブ配信サーチ\n5分ごとに更新します。終了するにはCtril + Cを押してください。")


# 動作環境の設定 windows | linux
os = "linux"
# 更新待機時間 (秒)
delay = 180

print("動作オペレーティングシステム："+os)

# tweepy
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
    videoTitle      = ""
    videoId         = ""
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
        streamingNumber = streamingNumber.replace(" Watching", "人")
        streamingNumber = streamingNumber.replace("K", "千")

        # 動画タイトルを抽出
        videoTitle = detail.find_all("a", id="video-title")[0].get("title")

        # 動画ID抽出
        videoURL = detail.find_all("a", class_=["yt-simple-endpoint.style-scope", "ytd-grid-video-renderer"])[0].get("href")
        videoId = videoURL.replace("/watch?v=", "")
    except:
        streamingNow = False

    return channelId, streamingNow, streamingNumber, videoTitle, videoId

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
            message = "[{}] {}さんのTwitterのアカウントが見つかりませんでした。".format(channelId, usrRoot["userName"])
            open("message.log", "a").write(message+"\n")
            print(message)

streamingData_before = []
def sort(play):
    # 既存のデータが新規のデータに含まれていた場合そのまま書き写す
    for strDa in streamingData_before:
        if strDa["channelId"] in str(streamingChannels):

            streamingData.append({ # 既存ライバー追加
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
                "videoId": strDa["videoId"],
                "play": strDa["play"]
            })

    # 書き込み用データにまだ含まれていない場合末尾に書く
    for strCha in streamingChannels:
        if strCha["channelId"] not in str(streamingData_before):

            streamingData.append({
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
                "videoId": strCha["videoId"],
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

def collab(videoTitle):
    collab_list = []
    for channelId in streamdata.keys():
        if streamdata[channelId]["userName"] in videoTitle: # 動画タイトルにライバー名が含まれていた場合
            collab_list.append(channelId)

    for channelId_collab in collab_list: # channelId_collab 追加するアカウント

        for cc_other in collab_list:
            if channelId_collab != cc_other: # channelId_collab（自分）以外 cc_other

                for cccheck in streamdata[channelId_collab]["collab"]: # 既に記録されているか
                    if cc_other == cccheck: break
                else: # コラボライバーを配列に記録
                    streamdata[channelId_collab]["collab"].append(cc_other)


while True:
    try:
        streamingChannels = [] # 取得したデータを書き込む
        streamingData     = [] # 書き込み用

        # YouTubeからデータを取得
        details = getSource()

        # スクレイピング
        for detail in details:
            channelId, streamingNow, streamingNumber, videoTitle, videoId = search(detail)

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
                        open("message.log", "a").write("未登録のライバー："+channelId+"\n")
                        channelId = "unregistered"

                if channelId != "unregistered": # 登録済みユーザーのみ

                    usrRoot = streamdata[channelId]

                    # タイトルにゲーム名がある場合取得
                    play = playGame(videoTitle)

                    # コラボ検出
                    collab(videoTitle)

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
                        "videoId": videoId,
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
            json.dump(streamingData, f)

        with open(settings.streamDataPath(os), "w") as f:
            json.dump(streamdata, f, indent=4)

        # データを保持　次のクロール時にデータを比較するため
        streamingData_before = streamingData

        # 3分間待機
        sleep(delay)

    except KeyboardInterrupt:
        print("キーが押されたので終了します。")
        driver.quit()
        break
    
    except Exception as e:
        print(str(e))
        open("error.log", "a").write(str(e)+"\n")
