import json, tweepy, settings, datetime

consumer_key='fOr1fbI9mCK1ztiqbEIMlHfLV'
consumer_secret='PdVL9Fb166jY7VMjXuA8EkjN4mWNlkEFI6XT3mTIEbqkVDGwMb'
access_key='4634604300-uYOEizJIhTQWMan2pLtfK9r73nXK5BK0h4rlwf3'
access_secret='54Dqdt8Kx7CoVKq2XqOSoTsKkTI7liPtpPugaZjGrTbRK'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth_handler=auth)

print(" - VTuberの情報をストリームデータに追加します。 -\nCtrl + Cで終了します。")

# 動作環境の設定 windows | linux
os = "linux"

print("動作オペレーティングシステム："+os)

with open(settings.streamDataPath(os), "r") as f:
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
        # TweepyでTwitterアイコン取得
        try:
            userStatus = api.get_user(input_twitterId)
            photo = userStatus.profile_image_url_https
            photo = photo.replace("_normal.jpg", "_400x400.jpg").replace("_normal.png", "_400x400.png")
        except:
            print("ユーザー情報が取得できませんでした。手動でアイコンURLを登録してください。")
            photo = input("TwitterアイコンURL：")

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
        data[input("チャンネルID：")] = userData
        userName.append(input_userName)
        print()
    except KeyboardInterrupt:
        input("\nエンターキーを押して終了します。")
        break

print("書き込み中")
with open(settings.streamDataPath(os), "w") as f:
    json.dump(data, f, indent=4)
print("書き込み完了")