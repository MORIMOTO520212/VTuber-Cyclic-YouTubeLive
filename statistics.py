# データ分析ツール
# 【オプション】
# livePointStatus   - ライブポイント状況
# iconUpdateCount   - アイコンアップデート状況
# games             - ゲームランキング
# collab            - コラボ人数状況
# videoTag          - 動画タイトルの【】内に入れている単語ランキング
# users             - 曜日ごとの配信者数ランキング
# timeUserNum       - 時間帯別視聴者数推移

import sys, json, glob, datetime

with open("database/streamdata.json", "r") as f:
    streamData = json.load(f)
channelIds = streamData.keys()
args = sys.argv

# ライブポイント状況
if "lp" == args[1]:
    csvData = ""
    for channelId in channelIds:
        livePointStatus = streamData[channelId]["livePointStatus"]
        csvData += ",".join(map(str, list(livePointStatus.values()))) + "\n"
    with open('livePointStatus.csv', 'w', encoding='utf-8') as f:
        f.write(csvData)
    print("complete!")


# アイコンアップデート状況
if "iu" == args[1]:
    for channelId in channelIds:
        print(streamData[channelId]["iconUpdateCount"])
    print("complete!")


# ゲームランキング
if "g" == args[1]:
    gameLst = {}
    for channelId in channelIds:
        games = streamData[channelId]["games"]
        for game in games:
            if game["product"] in gameLst:
                gameLst[game["product"]] += 1
            else:
                gameLst[game["product"]] = 1
    csvData = ""
    for product in gameLst.keys():
        csvData += f"\"{product}\",{gameLst[product]}\n"

    with open('games.csv', 'w', encoding='utf-8') as f:
        f.write(csvData)
    print("complete!")


# コラボ人数状況
if "c" == args[1]:
    for channelId in channelIds:
        print(len(streamData[channelId]["collab"]))
    print("complete!")


# 動画タイトルの【】内に入れている単語ランキング
if "vt" == args[1]:
    streamingsPath = glob.glob('log/streaming/*')
    videoTags = {}
    for streamingPath in streamingsPath:
        with open(streamingPath, 'r') as f:
            data = json.load(f)
            for d in data:
                for detail in d['details']:
                    videoTag = detail['videoTag']
                    if videoTag in videoTags.keys():
                        videoTags[videoTag] += 1
                    else:
                        videoTags[videoTag] = 1
    csvData = ""
    for videoTag in videoTags.keys():
        csvData += f"\"{videoTag}\",{videoTags[videoTag]}\n"

    with open('videoTag_ranking.csv', 'w', encoding='utf-8') as f:
        f.write(csvData)
    print("complete!")


# 曜日ごとの配信者数ランキング
if "u" == args[1]:
    streamings = glob.glob('log/streaming/*')

    data_day_of_week = {
        "Mon": [], "Tue": [], "Wed": [],
        "Thu": [], "Fri": [], "Sat": [],
        "Sun": []
    }

    for streaming in streamings:
        with open(streaming, 'r') as f:
            data = json.load(f)
        
        for record in data:
            timestamp = record['timestamp']
            dt = datetime.datetime.fromtimestamp(timestamp)
            day_of_week = dt.strftime('%a') # day of week
            data_day_of_week[day_of_week].append(record['users'])
    csvData = ""
    for day in data_day_of_week.keys():
        day_lst = data_day_of_week[day]
        users = sum(day_lst)/len(day_lst)
        csvData += f"\"{day}\",{round(users)}\n"

    with open('stream_ranking.csv', 'w', encoding='utf-8') as f:
        f.write(csvData)


# 時間帯別視聴者数推移
if "tu" == args[1]:
    streamings = glob.glob('log/streaming/*')

    data_hour = {
        "00": [], "01": [], "02": [],
        "03": [], "04": [], "05": [],
        "06": [], "07": [], "08": [],
        "09": [], "10": [], "11": [],
        "12": [], "13": [], "14": [],
        "15": [], "16": [], "17": [],
        "18": [], "19": [], "20": [],
        "21": [], "22": [], "23": [],
    }

    for streaming in streamings:
        with open(streaming, 'r') as f:
            data = json.load(f)

        for d in data:
            timestamp = d['timestamp']
            dt = datetime.datetime.fromtimestamp(timestamp)
            hour = dt.strftime('%H') # get day of week
            stack = []

            for detail in d['details']:
                streamingNumber = detail['streamingNumber']
                if "万人" in streamingNumber:
                    streamingNumber = float(streamingNumber.replace('万人', '')) * 10000
                elif "人" in streamingNumber:
                    streamingNumber = int(streamingNumber.replace('人', ''))
                stack.append(streamingNumber)
            
            data_hour[hour].extend(stack)

    for dowKey in data_hour.keys():
        streamingNumberAve = sum(data_hour[dowKey]) / len(data_hour[dowKey])
        print(f"{dowKey},{streamingNumberAve}")


# 曜日別視聴者数推移
if "du" == args[1]:
    streamings = glob.glob('log/streaming/*')

    data_day_of_week = {
        "Mon": [], "Tue": [], "Wed": [],
        "Thu": [], "Fri": [], "Sat": [],
        "Sun": []
    }

    for streaming in streamings:
        with open(streaming, 'r') as f:
            data = json.load(f)

        for d in data:
            timestamp = d['timestamp']
            dt = datetime.datetime.fromtimestamp(timestamp)
            day_of_week = dt.strftime('%a') # get day of week
            stack = []

            for detail in d['details']:
                streamingNumber = detail['streamingNumber']
                if "万人" in streamingNumber:
                    streamingNumber = float(streamingNumber.replace('万人', '')) * 10000
                elif "人" in streamingNumber:
                    streamingNumber = int(streamingNumber.replace('人', ''))
                stack.append(streamingNumber)
            
            data_day_of_week[day_of_week].extend(stack)

    for dowKey in data_day_of_week.keys():
        streamingNumberAve = sum(data_day_of_week[dowKey]) / len(data_day_of_week[dowKey])
        print(f"{dowKey},{streamingNumberAve}")


# 指定した日時に配信していたチャンネルを取り出す
# 範囲指定の場合は時間は書かない
# 例）2022年02月20日00時のチャンネルを取り出す場合
# 　　>glp 2022.02.20.00
if "glp" == args[1]:
    channelData = []
    setTime = args[2]
    setTime = setTime.split('.')
    print("set time length:", len(setTime))
    print(f"set time: {setTime[0]}/{setTime[1]}/{setTime[2]}")
    fileName = f"log/streaming/streamingLog_{setTime[0]+setTime[1]+setTime[2]}.json"

    with open(fileName, 'r') as f:
        data = json.load(f)
    print("open file:", fileName)
    print("open file: database/streamdata.json")
    
    print("----------- candidate -----------")

    for d in data:
        timestamp = d['timestamp']
        dt = datetime.datetime.fromtimestamp(timestamp)

        if dt.strftime('%Y.%m.%d.%H') == f"{setTime[0]}.{setTime[1]}.{setTime[2]}.{setTime[3]}":
            print("found:", dt.strftime('%Y.%m.%d.%H.%M'))

        if 4 == len(setTime): # 年月日時までの場合
            if dt.strftime('%Y.%m.%d.%H') == args[2]:
                for user in d['details']:
                    if not (user['channelId'] in [chid[2] for chid in channelData]):
                        channelId = user['channelId']
                        userName  = streamData[user['channelId']]['userName']
                        videoTitle = user['videoTitle'][:16]
                        channelData.append([userName, videoTitle, channelId])

        if 5 == len(setTime): # 年月日時分までの場合
            if dt.strftime('%Y.%m.%d.%H.%M') == args[2]:
                for user in d['details']:
                    if not (user['channelId'] in [chid[2] for chid in channelData]):
                        channelId = user['channelId']
                        videoTitle = user['videoTitle'][:16]
                        userName  = streamData[user['channelId']]['userName']
                        channelData.append([userName, videoTitle, channelId])
    
    print("----------- channel URL -----------")
    for chId in channelData:
        print(f"{chId[0]}\t\t{chId[1]}\t\thttps://www.youtube.com/channel/{chId[2]}")
    else:
        print("complete.")