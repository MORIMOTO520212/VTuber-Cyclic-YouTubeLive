import os, json, settings
#   Database Addition
#   streamdata.jsonへ新しいキーを追加する
#   追加したいキーと内容を入力してください
KEY = "twitterUserId"
VALUE = ""
#   {"KEY": "VALUE"}
#
if os.name == "nt": OS = "windows"
if os.name == "posix": OS = "linux"

print("動作オペレーティングシステム："+OS)

with open(settings.streamDataPath(OS), "r") as f:
    print("open file.")
    streamData = json.load(f)
    print("loaded file.")
try:
    for channelId in streamData.keys():
        streamData[channelId][KEY] = VALUE
    print("process complete.")
    with open(settings.streamDataPath(OS), "w") as f:
        json.dump(streamData, f, indent=4)
    print("dump.")
except Exception as e:
    print(str(e))