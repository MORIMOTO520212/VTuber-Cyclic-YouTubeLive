from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import json, settings, datetime


print("ライブ配信サーチ\n5分ごとに更新します。終了するにはCtril + Cを押してください。")


# 動作環境の設定 windows | linux
os = "linux"
# 更新待機時間 (秒)
delay = 120
# 名前解析　周辺にある文字から名前を特定する
true_noise_L = ["【", "・", "/", " ", "　"]
true_noise_R = ["先輩", "ちゃん", "】", "・", "/", " ", "　"]

print("動作オペレーティングシステム："+os)

print("selenium webdriver...")
# ヘッドレスモードでユーザープロファイルを使う
Options = webdriver.FirefoxOptions()
Options.headless = True #Options.set_headless() Linuxでは非推奨
PROFILE_PATH = settings.firefoxProfilePath(os)
Options.profile = PROFILE_PATH
driver = webdriver.Firefox(options=Options) # firefox_optionsはLinuxでは非推奨

print("complete!")

idChangeData = streamdata = gamesData = {}
def loadDataFiles():
    global idChangeData, streamdata, gamesData
    with open(settings.idChangeDataPath(os), "r") as f:
        idChangeData = json.load(f)
    with open(settings.streamDataPath(os), "r") as f:
        streamdata = json.load(f)
    with open(settings.gamesDataPath(os), "r") as f:
        gamesData = json.load(f)

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
        #streamingNumber = streamingNumber.replace(" 人が視聴中", "人")
        #streamingNumber = streamingNumber.replace("K", "千")
        #streamingNumber = streamingNumber.replace(" watching", "人")

        # 動画タイトルを抽出
        videoTitle = detail.find_all("a", id="video-title")[0].get("title")

        # 動画ID抽出
        videoURL = detail.find_all("a", class_=["yt-simple-endpoint.style-scope", "ytd-grid-video-renderer"])[0].get("href")
        videoId = videoURL.replace("/watch?v=", "")
    except:
        streamingNow = False

    return channelId, streamingNow, streamingNumber, videoTitle, videoId

streamingData_before = []
def sort():
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
        userName = streamdata[channelId]["userName"]
        namef_L = namef_R = False
        if userName in videoTitle: # 動画タイトルにライバー名が含まれていた場合
            if not videoTitle.split(userName)[0]: # 左端
                namef_L = True
            if not videoTitle.split(userName)[1]: # 右端
                namef_R = True
            for tn in true_noise_L:
                if tn + userName in videoTitle:
                    namef_L = True
            for tn in true_noise_R:
                if userName + tn in videoTitle:
                    namef_R = True
            if namef_L == True and namef_R == True:
                collab_list.append(channelId)

    for channelId_collab in collab_list: # channelId_collab 追加するアカウント

        for cc_other in collab_list:
            if channelId_collab != cc_other: # channelId_collab（自分）以外 cc_other

                for cccheck in streamdata[channelId_collab]["collab"]: # 既に記録されているか
                    if cc_other == cccheck: break
                else: # コラボライバーを配列に記録
                    streamdata[channelId_collab]["collab"].append(cc_other)


while True:
    # セマフォ確認
    while True:
        if "0" == open(".semaphore", "r").read(): sleep(60)
        else: break
    open(".semaphore", "w").write("0")
    try:
        streamingChannels = [] # 取得したデータを書き込む
        streamingData     = [] # 書き込み用

        loadDataFiles() # データをロード

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
                    
                    if channelId not in str(streamingChannels): # 同じユーザーを2度取得している場合がある
                        try:
                            usrRoot = streamdata[channelId]
                        except:
                            raise ValueError(channelId+" チャンネルが登録されていません。")

                        # タイトルにゲーム名がある場合取得
                        play = playGame(videoTitle)

                        # コラボ検出
                        collab(videoTitle)

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


        if streamingChannels != []: # （未完成）ライブ配信を誰もしていない場合は今後の予定を記録する
            # チャンネルデータのソート　新しいデータは末尾に追加する
            sort()

        print("取得チャンネル数：{}　配信者数：{}".format(str(len(details)), str(len(streamingChannels))))

        # 書き込み
        with open(settings.streamingDataPath(os), "w") as f:
            json.dump(streamingData, f, indent=4)

        with open(settings.streamDataPath(os), "w") as f:
            json.dump(streamdata, f, indent=4)

        # データを保持　次のクロール時にデータを比較するため
        streamingData_before = streamingData

        # 3分間待機
        open(".semaphore", "w").write("1")
        sleep(delay)

    except KeyboardInterrupt:
        print("キーが押されたので終了します。")
        open(".semaphore", "w").write("1")
        driver.quit()
        break
    
    except Exception as e:
        print("main Error: "+str(e))
        open("error.log", "a").write(str(e)+"\n")
        open(".semaphore", "w").write("1")