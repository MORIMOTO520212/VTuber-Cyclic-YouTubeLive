import json

with open("database/streamdata.json", "r") as f:
    data = json.load(f)

try:
    for channelId in data:
            try:
                print(data[channelId]["userName"]+" >"+data[channelId]["photo"])
            except:
                link = input(data[channelId]["twitterId"]+" >")
                data[channelId]["photo"] = link
except KeyboardInterrupt:
    print("キーが押されたので終了します。")

with open("database/streamdata.json", "w") as f:
    json.dump(data, f, indent=4)