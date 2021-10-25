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
        