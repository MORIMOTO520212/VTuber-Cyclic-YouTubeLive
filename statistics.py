import sys, json, glob

with open("database/streamdata.json", "r") as f:
    streamData = json.load(f)
channelIds = streamData.keys()
args = sys.argv

# ライブポイント状況
if "livePointStatus" == args[1]:
    csvData = ""
    for channelId in channelIds:
        livePointStatus = streamData[channelId]["livePointStatus"]
        csvData += ",".join(map(str, list(livePointStatus.values()))) + "\n"
    with open('livePointStatus.csv', 'w', encoding='utf-8') as f:
        f.write(csvData)
    print("complete!")


# アイコンアップデート状況
if "iconUpdateCount" == args[1]:
    for channelId in channelIds:
        print(streamData[channelId]["iconUpdateCount"])
    print("complete!")


# ゲームランキング
if "games" == args[1]:
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
if "collab" == args[1]:
    for channelId in channelIds:
        print(len(streamData[channelId]["collab"]))
    print("complete!")


# 動画タイトルの【】内に入れている単語ランキング
if "videoTag" == args[1]:
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