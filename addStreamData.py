import json

print("VTuberの情報をストリームデータに追加します。")

with open("database/streamdata.json", "r") as f:
    data = json.load(f)

while True:
    try:
        userData = {}
        userData["userName"]  = input("ユーザー名：")
        userData["twitterId"] = input("Twitter ID：")
        data[input("チャンネルID：")] = userData
        print()
    except KeyboardInterrupt:
        input("\nエンターキーを押して終了します。")
        break

print("書き込み中")
with open("database/streamdata.json", "w") as f:
    json.dump(data, f, indent=4)
print("書き込み完了")