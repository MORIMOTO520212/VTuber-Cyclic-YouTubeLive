import sys, json

with open("database/streamdata.json", "r") as f:
    streamData = json.load(f)
channelIds = streamData.keys()
args = sys.argv

# get livePointStatus
if "livePointStatus" == args[1]:
    for channelId in channelIds:
        livePointStatus = streamData[channelId]["livePointStatus"]
        print(",".join(map(str, list(livePointStatus.values()))))


# get iconUpdateCount
if "iconUpdateCount" == args[1]:
    for channelId in channelIds:
        print(streamData[channelId]["iconUpdateCount"])

# get games
if "games" == args[1]:
    gameLst = {}
    for channelId in channelIds:
        games = streamData[channelId]["games"]
        for game in games:
            if game["product"] in gameLst:
                gameLst[game["product"]] += 1
            else:
                gameLst[game["product"]] = 1
    for product in gameLst.keys():
        print(f"\"{product}\",{gameLst[product]}")

# get collab
if "collab" == args[1]:
    for channelId in channelIds:
        print(len(streamData[channelId]["collab"]))