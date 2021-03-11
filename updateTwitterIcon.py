# updateTwitterIcon.py
# ライバーのTwitterアイコンを定期的にチェックし、URLの有効期限が切れていた場合更新します。
# Created : 2020/10/29
import os, json, settings, tweepy, datetime
from time import sleep

# 動作環境
if os.name == "nt": OS = "windows"
if os.name == "posix": OS = "linux"
# 更新間隔(秒)
delay = 3600*12 # 12時間

print("updateTwitterIcon.py")
print("ライバーのTwitterアイコンを定期的にチェックし、URLの有効期限が切れていた場合更新します。")
print("Created : 2020/10/29")
consumer_key, consumer_secret, access_key, access_secret = settings.tweepyKeyPath()
print("tweepy API...")
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth_handler=auth)

def main():
    try:
        with open(settings.streamDataPath(OS), "r") as f:
            streamdata = json.load(f)

        for channelId in streamdata.keys():
            now = datetime.datetime.now()
            usrRoot = streamdata[channelId]
            try:
                print(usrRoot["userName"])
                userStatus = api.get_user(usrRoot["twitterId"])
                photo = userStatus.profile_image_url_https
                photo = photo.replace("_normal.jpg", "_400x400.jpg").replace("_normal.png", "_400x400.png")
                if photo != usrRoot["photo"]:
                    usrRoot["photo"] = photo
                    usrRoot["iconUpdateCount"] += 1
                    # 最終アイコンアップデート日
                    usrRoot["lastIconUpdateDate"] = now.strftime("%Y/%m/%d %H:%M:%S")
                    
                    message = "{} [UTI] {}さんのアイコンデータを更新しました.\n".format(now.strftime("%Y/%m/%d %H:%M:%S"), usrRoot["userName"])
                    open(settings.messageLogPath(OS), "a").write(message)
                    print(usrRoot["userName"]+"さんのアイコンデータを更新しました.")
            except Exception as e:
                if "User not found" in str(e): # Twitterアカウントが見つからなかった場合
                    message = "{} [UTI] \"{}\" {}さんのTwitterのアカウントが見つかりませんでした.\n".format(now.strftime("%Y/%m/%d %H:%M:%S"), channelId, usrRoot["userName"])
                    open(settings.messageLogPath(OS), "a").write(message)
                    print(message)
                else:
                    open(settings.errorLogPath(OS), "a").write("{} [UTI] {}".format(now.strftime("%Y/%m/%d %H:%M:%S"), str(e)))
            sleep(1)
        return streamdata
    except Exception as e:
        print(str(e))
        open(".semaphore", "w").write("1")
        exit()

while True:
    # セマフォ確認
    while True:
        if "0" == open(".semaphore", "r").read(): sleep(60)
        else: break
    open(".semaphore", "w").write("0")

    try:
        streamdata = main() # 更新したデータを返す
        with open(settings.streamDataPath(OS), "w") as f:
            json.dump(streamdata, f, indent=4) # 保存
        now = datetime.datetime.now()
        open(settings.messageLogPath(OS), "a").write("{} [UTI] アイコンアップデート完了.\n".format(now.strftime("%Y/%m/%d %H:%M:%S")))

        open(".semaphore", "w").write("1")
        print("待機中...")
        sleep(delay)
    except KeyboardInterrupt:
        print("キーが押されたので終了します.")
        open(".semaphore", "w").write("1")
        exit()