import json, tweepy, settings, datetime

consumer_key, consumer_secret, access_key, access_secret = settings.tweepyKeyPath()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth_handler=auth)

print(" - VTuberの情報をストリームデータに追加します。 -\nCtrl + Cで終了します。")
print("自動登録する場合はchannels.txtファイルを作成し、名前, TwitterID, チャンネルIDの順に改行を入れて保存してください。\n")

# 動作環境の設定 windows | linux
if "1" == input("Windowsを使っている場合は1, Linuxの場合は2："):
    os = "windows"
else:
    os = "linux"

print("動作オペレーティングシステム："+os)

with open(settings.streamDataPath(os), "r") as f:
    data = json.load(f)
userName = []
for channelId in data:
    userName.append(data[channelId]["userName"])

print("登録済ライバー数："+str(len(userName)))

def add(in_userName, in_twitterId, photo, channelId):
    userData = {}
    now = datetime.datetime.now()
    userData["userName"]  = in_userName
    userData["twitterId"] = in_twitterId
    userData["photo"]     = photo
    userData["livePoint"] = 0
    userData["lastLiveDate"] = now.strftime("%Y/%m/%d %H:%M:%S")
    userData["iconUpdateCount"] = 0
    userData["lastIconUpdateDate"] = now.strftime("%Y/%m/%d %H:%M:%S")
    userData["livePointStatus"] =  {
        "00": 0, "01": 0, "02": 0, "03": 0,
        "04": 0, "05": 0, "06": 0, "07": 0,
        "08": 0, "09": 0, "10": 0, "11": 0,
        "12": 0, "13": 0, "14": 0, "15": 0,
        "16": 0, "17": 0, "18": 0, "19": 0,
        "20": 0, "21": 0, "22": 0, "23": 0
    }
    userData["games"]  = []
    userData["collab"] = []
    data[channelId] = userData
    userName.append(in_userName)

if 1 == input("手動で入力する場合は1, リスト形式の場合は2："):
    while True:
        try:
            userData = {}
            channelId = input("チャンネルID：")
            in_twitterId = input("Twitter ID：")
            in_userName  = input("ユーザー名：")
            if in_userName in userName:
                print("同じ名前のユーザーが既に登録済です。\n")
                continue

            try: # TweepyでTwitterアイコン取得
                userStatus = api.get_user(in_twitterId)
                photo = userStatus.profile_image_url_https
                photo = photo.replace("_normal.jpg", "_400x400.jpg").replace("_normal.png", "_400x400.png")
            except:
                print("ユーザー情報が取得できませんでした。手動でアイコンURLを登録してください。")
                photo = input("TwitterアイコンURL：")

            add(in_userName, in_twitterId, photo, channelId)
            print()

        except KeyboardInterrupt:
            input("\nエンターキーを押して終了します。")
            break
else:
    while True:
        try:
            with open("channels.txt", "r", encoding="utf-8") as f:
                channeladd = f.read()
            channels = channeladd.split("\n")
            i = 0
            userData = {}
            while i < len(channels)-1:
                input_userName = channels[i]

                if input_userName in userName:
                    print(input_userName, "既に登録済みのユーザーです。\n")
                    continue
                
                print(input_userName)

                i += 1
                input_twitterId = channels[i]
                # TweepyでTwitterアイコン取得
                try:
                    userStatus = api.get_user(input_twitterId)
                    photo = userStatus.profile_image_url_https
                    photo = photo.replace("_normal.jpg", "_400x400.jpg").replace("_normal.png", "_400x400.png")
                except:
                    print(input_userName, "ユーザー情報が取得できませんでした。手動でアイコンURLを登録してください。")
                    photo = input("TwitterアイコンURL：")
                
                print(input_twitterId)

                userData["userName"]  = input_userName
                userData["twitterId"] = input_twitterId
                userData["photo"]     = photo
                now = datetime.datetime.now()
                userData["livePoint"] = 0
                userData["lastLiveDate"] = now.strftime("%Y/%m/%d %H:%M:%S")
                userData["iconUpdateCount"] = 0
                userData["lastIconUpdateDate"] = now.strftime("%Y/%m/%d %H:%M:%S")
                userData["livePointStatus"] =  {
                    "00": 0, "01": 0, "02": 0, "03": 0,
                    "04": 0, "05": 0, "06": 0, "07": 0,
                    "08": 0, "09": 0, "10": 0, "11": 0,
                    "12": 0, "13": 0, "14": 0, "15": 0,
                    "16": 0, "17": 0, "18": 0, "19": 0,
                    "20": 0, "21": 0, "22": 0, "23": 0
                }
                userData["games"]  = []
                userData["collab"] = []
                
                i += 1
                data[channels[i]] = userData
                userName.append(input_userName)

                print(channels[i])
                print("-------------------------------------------")
                
                i += 1
        except KeyboardInterrupt:
            input("\nエンターキーを押して終了します。")
            break
        
        if "n" == input("この情報でよろしいですか。y/n："):
            exit()
        break

print("書き込み中")
with open(settings.streamDataPath(os), "w") as f:
    json.dump(data, f, indent=4)
print("書き込み完了")