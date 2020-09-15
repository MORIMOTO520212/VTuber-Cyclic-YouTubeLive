import json

print(" - VTuberの情報をストリームデータに追加します。 -\nCtrl + Cで終了します。")

with open("setting.json", "r") as f:
    setting = json.load(f)

with open(setting["streamingPath"], "r") as f:
    data = json.load(f)

userName = []
for channelId in data:
        userName.append(data[channelId]["userName"])

print("登録済ライバー数："+str(len(userName)))
while True:
    try:
        userData = {}
        input_userName  = input("ユーザー名：")
        if input_userName in userName:
            print("既に登録済みのユーザーです。\n")
            continue
        input_twitterId = input("Twitter ID：")
        input_photo     = input("TwitterアイコンURL：")
        userData["userName"]  = input_userName
        userData["twitterId"] = input_twitterId
        userData["photo"]     = input_photo
        data[input("チャンネルID：")] = userData
        userName.append(input_userName)
        print()
    except KeyboardInterrupt:
        input("\nエンターキーを押して終了します。")
        break

print("書き込み中")
with open("database/streamdata.json", "w") as f:
    json.dump(data, f, indent=4)
print("書き込み完了")