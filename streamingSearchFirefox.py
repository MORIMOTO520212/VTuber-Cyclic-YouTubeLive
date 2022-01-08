from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import re, os, json, time, settings, datetime

print("ライブ配信サーチ\n3分ごとに更新します。終了するにはCtril + Cを押してください。")

# 動作環境の設定 windows | linux
if os.name == "nt": OS = "windows"
if os.name == "posix": OS = "linux"
# 更新待機時間 (秒)
delay = 120
# 名前解析　周辺にある文字から名前を特定する
true_noise_L = ["【", "・", "/", " ", "　"]
true_noise_R = ["先輩", "ちゃん", "】", "・", "/", " ", "　"]

print("動作オペレーティングシステム："+OS)

# streamingDataの初期化
print("cleanup streamingData...")
with open(settings.streamingDataPath(OS), "w") as f:
    json.dump([], f)

# スタートアップメッセージ
print("complete!")
now = datetime.datetime.now()
open(settings.messageLogPath(OS), "a").write("{} ---- run streamingSearchFirefox.py ----\n".format(now.strftime("%Y/%m/%d %H:%M:%S")))

driver = None
streamingData_before = []
idChangeData = streamdata = gamesData = {}

def loadDataFiles():
    'データを読み込む'
    global idChangeData, streamdata, gamesData, streamingData_before
    with open(settings.idChangeDataPath(OS), "r") as f:  # idChangeData.json
        idChangeData = json.load(f)
    with open(settings.streamDataPath(OS), "r") as f:    # streamdata.json
        streamdata = json.load(f)
    with open(settings.gamesDataPath(OS), "r") as f:     # games.json
        gamesData = json.load(f)
    with open(settings.streamingDataPath(OS), "r") as f: # streamdata.json
        streamingData_before = json.load(f)

def writeLog(type, msg):
    now = datetime.datetime.now()
    if "message" == type:
        open(settings.messageLogPath(OS), "a").write("{} [SSF] {}\n".format(now.strftime("%Y/%m/%d %H:%M:%S"), str(msg)))
    if "error" == type:
        open(settings.errorLogPath(OS), "a").write("{} [SSF] {}\n".format(now.strftime("%Y/%m/%d %H:%M:%S"), str(msg)))

def getSource():
    'YouTubeからデータをスクレイピングする'
    global driver
    
    print("getSource: driver get.")
    # ヘッドレスモードでユーザープロファイルを使う
    Options = webdriver.FirefoxOptions()
    Options.headless = True #Options.set_headless() Linuxでは非推奨
    PROFILE_PATH = settings.firefoxProfilePath(OS)
    Options.profile = PROFILE_PATH
    driver = webdriver.Firefox(options=Options) # ドライバー起動 firefox_optionsはLinuxでは非推奨
    driver.get("https://www.youtube.com/feed/subscriptions")

    # 2つ目のチャンネルブロックを取得するために最下部までスクロール
    print("getSource: window scroll.")
    driver.execute_script("window.scrollTo(0, 5000);")
    soup = ""
    for _ in range(5): # スクロールの検出とソースの取得　タイムアウト時間最大50秒
        sleep(10)
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        channelbrock = soup.find_all("ytd-item-section-renderer", class_=["style-scope", "ytd-section-list-renderer"])
        if 2 == len(channelbrock): break
        else:
            driver.save_screenshot("screenshot.png")
            print("再試行{}：2つのチャンネルブロックのロードが完了しませんでした。".format(str(_+1)))
            writeLog('error', f'{str(_+1)}：2つのチャンネルブロックのロードが完了しませんでした。\n')
            driver.execute_script("window.scrollTo(0, 1000);")

    print("getSource: find all div tag.")
    details = soup.find_all("div", id="details")
    driver.quit()

    return details

def search(detail):
    '配信者のデータを抽出する'
    streamingNumber = ""
    videoTitle      = ""
    videoId         = ""
    thumbnailUrl    = ""
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
        streamingNumber = streamingNumber.replace("K", "千")
        streamingNumber = streamingNumber.replace(" watching", "人")

        # 動画タイトルを抽出
        videoTitle = detail.find_all("a", id="video-title")[0].get("title")

        # 動画ID抽出
        videoUrl = detail.find_all("a", class_=["yt-simple-endpoint.style-scope", "ytd-grid-video-renderer"])[0].get("href")
        videoId = videoUrl.replace("/watch?v=", "")

        # サムネイルリンクの抽出
        thumbnailUrl = f"https://i.ytimg.com/vi/{videoId}/hqdefault_live.jpg"
    except:
        streamingNow = False

    return channelId, streamingNow, streamingNumber, videoTitle, videoId, thumbnailUrl

def sort():
    'チャンネルデータのソート　新しいデータは末尾に追加する'
    global streamingChannels, streamingData_before

    # 既存のデータが新規のデータに含まれていた場合そのまま書き写す
    for strDa in streamingData_before:
        if strDa["channelId"] in str(streamingChannels):

            # 既存データの視聴者数・ライブポイント・動画タイトルを更新
            streamingNumber = False
            livePoint       = False
            videoTitle      = False
            for liver in streamingChannels:
                if strDa["channelId"] == liver["channelId"]:
                    streamingNumber = liver["streamingNumber"]
                    livePoint       = liver["livePoint"]
                    videoTitle      = liver["videoTitle"]

            streamingData.append({ # 既存ライバー追加
                "channelId": strDa["channelId"],
                "userName": strDa["userName"],
                "twitterId": strDa["twitterId"],
                "active_badge": strDa["active_badge"],
                "streamingNumber": streamingNumber,
                "videoTitle": videoTitle,
                "photo": strDa["photo"],
                "livePoint": livePoint,
                "lastLiveDate": strDa["lastLiveDate"],
                "iconUpdateCount": strDa["iconUpdateCount"],
                "lastIconUpdateDate": strDa["lastIconUpdateDate"],
                "livePointStatus" : strDa["livePointStatus"],
                "videoId": strDa["videoId"],
                "play": strDa["play"],
                "thumbnailUrl": strDa["thumbnailUrl"]
            })

    # 書き込み用データにまだ含まれていない場合末尾に書く
    for strCha in streamingChannels:
        if strCha["channelId"] not in str(streamingData_before):

            streamingData.append({ # 現在取得したライバー追加
                "channelId": strCha["channelId"],
                "userName": strCha["userName"],
                "twitterId": strCha["twitterId"],
                "active_badge": strCha["active_badge"],
                "streamingNumber": strCha["streamingNumber"],
                "videoTitle": strCha["videoTitle"],
                "photo": strCha["photo"],
                "livePoint": strCha["livePoint"],
                "lastLiveDate": strCha["lastLiveDate"],
                "iconUpdateCount": strCha["iconUpdateCount"],
                "lastIconUpdateDate": strCha["lastIconUpdateDate"],
                "livePointStatus" : strCha["livePointStatus"],
                "videoId": strCha["videoId"],
                "play": strCha["play"],
                "thumbnailUrl": strCha["thumbnailUrl"]
            })

def playGame(videoTitle):
    'タイトルにゲーム名がある場合抽出する'
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
    'ユーザーの登録情報を更新する'
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
                game["lastPlayDate"] = now.strftime("%Y/%m/%d %H:%M:%S")
                break
        else:
            usrRoot["games"].append(play)

def collab(videoTitle):
    '動画のタイトルからコラボを検出する'
    collab_list = [] # コラボしたアカウントリスト
    status_collab = False # コラボが検出されればTrue
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
                status_collab = True

    for channelId_collab in collab_list: # channelId_collab 追加するアカウント

        for cc_other in collab_list:
            if channelId_collab != cc_other: # channelId_collab（自分）以外 cc_other

                for cccheck in streamdata[channelId_collab]["collab"]: # 既に記録されているか
                    if cc_other == cccheck: break
                else: # コラボライバーを配列に記録
                    streamdata[channelId_collab]["collab"].append(cc_other)
    return status_collab

def activBadgeCheck():
    'アクティブバッジを更新する'
    i=0
    while i < len(streamingData_before):
        channelId = streamingData_before[i]["channelId"]
        active_badge = streamingData_before[i]["active_badge"]
        streamdata[channelId]["active_badge"] = active_badge
        i += 1

def streamingLog(streamingChannels):
    # リアルタイムログの記録
    print("write streaming log.")
    now = datetime.datetime.now() # 年月日
    fileName = settings.streamingLogPath(OS) + f'/streamingLog_{now.strftime("%Y%m%d")}.json'

    is_file = os.path.isfile(fileName)
    if is_file:
        with open(fileName, 'r') as f:
            streamingLogData = json.load(f)
    else:
        streamingLogData = []

    newDict = {}
    newDict["timestamp"] = int(time.time())   # 記録時間
    newDict["users"] = len(streamingChannels) # 配信者数
    newDict["details"] = []

    for channel in streamingChannels:
        channelId  = channel["channelId"]     # チャンネルID
        videoTitle = channel["videoTitle"]
        pattern    = "(?<=【).+?(?=】)"

        res = re.findall(pattern, videoTitle) #【】内の文字列
        if res:
            videoTag = res[0]
        else:
            videoTag = False

        play = channel["play"] # プレイゲーム名　無効な場合はFalse
        if play:
            productName = play["product"]
        else:
            productName = False
            
        newDict["details"].append({
            "channelId": channelId,
            "videoTag": videoTag,
            "videoTitle": videoTitle,
            "streamingNumber": channel["streamingNumber"], # 同時接続者数
            "livePoint": channel["livePoint"], # ライブポイント
            "play": productName
        })

    streamingLogData.append(newDict)

    with open(fileName, 'w') as f:
        json.dump(streamingLogData, f, indent=4)


while True:
    # セマフォ確認
    while True:
        if "0" == open(".semaphore", "r").read():
            print("処理待機")
            sleep(60)
        else: break
    open(".semaphore", "w").write("0")
    try:
        streamingChannels = [] # 取得したデータを書き込む
        streamingData     = [] # 書き込み用

        print("load data files.")
        loadDataFiles()

        print("get youtube source.")
        details = getSource()

        # スクレイピング
        print("process channels.")
        for detail in details:
            channelId, streamingNow, streamingNumber, videoTitle, videoId, thumbnailUrl = search(detail)

            if streamingNow == "ライブ配信中" or streamingNow == "LIVE NOW":
                # 登録済か未登録か
                for channelIdData in streamdata.keys():
                    if channelIdData == channelId:
                        break
                else:
                    try: channelId = idChangeData[channelId] # ユーザーIDでチャンネルIDが取得できた場合
                    except:
                        print("未登録のライバー："+channelId)
                        writeLog('message', f'未登録のライバー：\"{channelId}\"\n')
                        channelId = 'unregistered'

                if channelId != 'unregistered': # 登録済みユーザーのみ
                    
                    if channelId not in str(streamingChannels): # 同じユーザーを2度取得している場合がある
                        try:
                            usrRoot = streamdata[channelId]
                        except:
                            writeLog('error', f'\"{channelId}\" idChangeDataにしか登録されていません.')
                            continue

                        play = playGame(videoTitle)

                        status_collab = collab(videoTitle)

                        streamingChannels.append({ # ストリーミングに追加
                            "channelId": channelId,
                            "userName": usrRoot["userName"],
                            "twitterId": usrRoot["twitterId"],
                            "active_badge": usrRoot["active_badge"],
                            "streamingNumber": streamingNumber,
                            "videoTitle": videoTitle,
                            "photo": usrRoot["photo"],
                            "livePoint": usrRoot["livePoint"],
                            "lastLiveDate": usrRoot["lastLiveDate"],
                            "iconUpdateCount": usrRoot["iconUpdateCount"],
                            "lastIconUpdateDate": usrRoot["lastIconUpdateDate"],
                            "livePointStatus" : usrRoot["livePointStatus"],
                            "videoId": videoId,
                            "play": play,
                            "thumbnailUrl": thumbnailUrl
                        })

                        # ライバーステータス更新
                        updateStatus(usrRoot, play)

        if streamingChannels != []: # 配信者がいた場合
            print("sort channel.")
            sort() # 並び替え
            activBadgeCheck() # 有効ユーザーの確認
            streamingLog(streamingChannels) # リアルタイムログ記録

        print(f"取得チャンネル数：{len(details)}　配信者数：{len(streamingChannels)}")

        # 書き込み
        print("write log.")
        with open(settings.streamingDataPath(OS), 'w') as f:
            json.dump(streamingData, f)

        with open(settings.streamDataPath(OS), 'w') as f:
            json.dump(streamdata, f, indent=4)

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
        if "Tried to run command without establishing a connection" in str(e):
            writeLog('message', 'geckodriverのバージョンが古い可能性があります。\n終了します。')
            open(".semaphore", "w").write('1')
            driver.quit()
            exit("geckodriverのバージョンが古い可能性があります。\n終了します。")

        writeLog('error', f'{str(e)}\n')
        open(".semaphore", "w").write("1")