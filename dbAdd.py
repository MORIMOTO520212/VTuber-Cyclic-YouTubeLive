import os, json, settings
#   streamdata.jsonへ新しいキーを追加する
#   追加したいキーと内容を入力してください
KEY = "active_badge"
VALUE = True

if os.name == "nt": OS = "windows"
if os.name == "posix": OS = "linux"

print("動作オペレーティングシステム："+OS)

with open(settings.streamDataPath(os), "r") as f:
    print("open file.")
    streamData = json.load(f)
try:
    for channelId in streamData.keys():
        streamData[channelId][KEY] = VALUE
    print("process complete.")
    with open(settings.streamDataPath(os), "w") as f:
        json.dump(streamData, f, indent=4)
except Exception as e:
    print(str(e))