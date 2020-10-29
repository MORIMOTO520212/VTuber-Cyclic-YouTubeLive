# updateTwitterIcon.py
# ライバーのTwitterアイコンを定期的にチェックし、URLの有効期限が切れていた場合更新します。
# Created : 2020/10/29
import json, requests, settings, tweepy, datetime
from time import sleep

# 動作環境
os = "windows"
# 更新間隔(秒)
delay = 3600*24

print("updateTwitterIcon.py")
print("ライバーのTwitterアイコンを定期的にチェックし、URLの有効期限が切れていた場合更新します。")
print("Created : 2020/10/29")
consumer_key, consumer_secret, access_key, access_secret = settings.tweepyKeyPath()
print("tweepy API...")
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth_handler=auth)
streamdata = {}

def main():
    try:
        with open(settings.streamDataPath(os), "r") as f:
            streamdata = json.load(f)

        now = datetime.datetime.now()

        for channelId in streamdata.keys():
            
            usrRoot = streamdata[channelId]
            if 200 != requests.get(usrRoot["photo"]).status_code:
                print(usrRoot["userName"]+" Status Code:404")
                try:
                    userStatus = api.get_user(usrRoot["twitterId"])
                    photo = userStatus.profile_image_url_https
                    usrRoot["photo"] = photo.replace("_normal.jpg", "_400x400.jpg").replace("_normal.png", "_400x400.png")
                    usrRoot["iconUpdateCount"] += 1
                    # 最終アイコンアップデート日
                    usrRoot["lastIconUpdateDate"] = now.strftime("%Y/%m/%d %H:%M:%S")
                    print(usrRoot["userName"]+"さんのアイコンデータを更新しました。")
                except Exception as e:
                    if "User not found" in str(e): # Twitterアカウントが見つからなかった場合
                        message = "[{}] {}さんのTwitterのアカウントが見つかりませんでした。".format(channelId, usrRoot["userName"])
                        open("message.log", "a").write("[UpdateTwitterIcon.py] "+message+"\n")
                        print(message)
            else:
                print(usrRoot["userName"]+" Status Code:200")
            
            sleep(0.5)

    except InterruptedError:
        print("キーが押されたので終了します。")
        exit()

while True:
    # セマフォ確認
    while True:
        if "0" == open(".semaphore", "r"): sleep(60)
        else: break
    open(".semaphore", "w").write("0")
    main()
    with open(settings.streamDataPath(os), "w") as f:
        json.dump(streamdata, f, indent=4)
    open(".semaphore", "w").write("1")
    print("待機中...")
    sleep(delay)