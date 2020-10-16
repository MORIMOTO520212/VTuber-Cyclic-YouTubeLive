import json, settings

os = "windows"

print("動作オペレーティングシステム："+os)

with open(settings.streamDataPath(os), "r") as f:
    streamData = json.load(f)

for channelId in streamData.keys():
    streamData[channelId]["collab"] = []

with open(settings.streamDataPath(os), "w") as f:
    json.dump(streamData, f, indent=4)
