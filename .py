import datetime, setting, json

with open(setting.streamDataPath(), "r") as f:
    streamData = json.load(f)

now = datetime.datetime.now()

for channelId in streamData.keys():
    streamData[channelId]["livePoint"] = 0
    streamData[channelId]["lastLiveDate"] = now.strftime("%Y/%m/%d %H:%M:%S")
    streamData[channelId]["iconUpdateCount"] = 0
    streamData[channelId]["lastIconUpdateDate"] = now.strftime("%Y/%m/%d %H:%M:%S")


with open(setting.streamDataPath(), "w") as f:
    json.dump(streamData, f, indent=4)