import os, json, tweepy, settings, datetime
from module import twitter_user_id as tui

consumer_key, consumer_secret, access_key, access_secret = settings.tweepyKeyPath() # settings.py -> tweepyKeyPath()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth_handler=auth)

print(" - VTuberの情報をストリームデータに追加します。 -\nCtrl + Cで終了します。")
print("自動登録する場合はchannels.txtファイルを作成し、名前, TwitterID, チャンネルIDの順に改行を入れて保存してください。\n")

# 動作環境の設定 windows | linux
if os.name == "nt": OS = "windows"
if os.name == "posix": OS = "linux"

print("動作オペレーティングシステム："+OS)

with open(settings.streamDataPath(OS), "r") as f:
    data = json.load(f)
userName = []
for channelId in data:
    userName.append(data[channelId]["userName"])

print("登録済ライバー数："+str(len(userName)))

def add(in_userName, in_twitterId, photo, channelId, twitterUserId):
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
    userData["active_badge"] = True
    userData["twitterUserId"] = twitterUserId
    data[channelId] = userData
    userName.append(in_userName)

if 1 == int(input("手動で入力する場合は1, リスト形式の場合は2：")):
    # 手動処理
    while True:
        try:
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
            
            twitterUserId = tui.getTwitterUserId(in_twitterId)
            if not twitterUserId:
                print("Twitter User Idがidtwi.comから取得できませんでした。")
                print("Twitter ID:",in_twitterId)
                twitterUserId = input("Twitter User Idを手動で入力してください >")

            add(in_userName, in_twitterId, photo, channelId, twitterUserId)
            print()

        except KeyboardInterrupt:
            input("\nエンターキーを押して終了します。")
            break
else:
    # リスト処理
    try:
        channeladd = open("channels.txt", "r", encoding="utf-8").read()
        channels = channeladd.split("\n")
        i = 0

        while i < len(channels)-1:
            in_userName = channels[i]

            i += 1 # 2 TwitterId
            in_twitterId = channels[i]
            # TweepyでTwitterアイコン取得
            try:
                userStatus = api.get_user(in_twitterId)
                photo = userStatus.profile_image_url_https
                photo = photo.replace("_normal.jpg", "_400x400.jpg").replace("_normal.png", "_400x400.png")
            except:
                print(in_userName, "ユーザー情報が取得できませんでした。手動でアイコンURLを登録してください。")
                photo = input("TwitterアイコンURL：")

            twitterUserId = tui.getTwitterUserId(in_twitterId)
            if not twitterUserId:
                print("Twitter User Idがidtwi.comから取得できませんでした。")
                print("Twitter ID:",in_twitterId)
                twitterUserId = input("Twitter User Idを手動で入力してください >")

            i += 1 # 3 ChannelId
            print(in_userName)
            print(in_twitterId)
            print(channels[i])
            print("-------------------------------------------")

            if in_userName in userName:
                print(in_userName, "既に登録済みのユーザーです。")
            else:
                add(in_userName, in_twitterId, photo, channels[i], twitterUserId)
            i += 1
    except KeyboardInterrupt:
        input("\nエンターキーを押して終了します。")
        exit()
    

if "y" == input("この情報でよろしいですか。y/n："):
    print("書き込み中")
    with open(settings.streamDataPath(OS), "w") as f:
        json.dump(data, f, indent=4)
    print("書き込み完了")