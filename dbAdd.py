import json, settings

# streamdata.jsonへ新しいキーを追加する #

os = "windows"

print("動作オペレーティングシステム："+os)

with open(settings.streamDataPath(os), "r") as f:
    streamData = json.load(f)

for channelId in streamData.keys():
    # --- ここへ追加したいキーを記述する --- #
    streamData[channelId]["collab"] = []

with open(settings.streamDataPath(os), "w") as f:
    json.dump(streamData, f, indent=4)
