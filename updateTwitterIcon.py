# updateTwitterIcon.py
# Description: ライバーのTwitterアイコンを定期的にチェックし、URLの有効期限が切れていた場合更新します。
# Created: 2020.10.29
# Update: 2021.12.27
# Author: YUMA.morimoto
import os, json, settings, tweepy, datetime
from module import twitter_user_id as tui
from time import sleep

# 動作環境
if os.name == "nt": OS = "windows"
if os.name == "posix": OS = "linux"
# 更新間隔（秒）
delay = 3600*12 # 12時間待機
# クロールの分割
segment = 0

print("updateTwitterIcon.py")
print("ライバーのTwitterアイコンを定期的にチェックし、URLの有効期限が切れていた場合更新します.")
print("Created : 2020/10/29")
consumer_key, consumer_secret = settings.tweepyKeyPath()
print("load tweepy API...")
auth = tweepy.OAuth2AppHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)

print("complete.")

def writeLog(type, msg):
    now = datetime.datetime.now()
    if 'message' == type:
        open(settings.messageLogPath(OS), "a").write(
            f'{now.strftime("%Y/%m/%d %H:%M:%S")} [UTI] ' + msg)
    if 'error' == type:
        open(settings.errorLogPath(OS), "a").write(
            f'{now.strftime("%Y/%m/%d %H:%M:%S")} [UTI] ' + msg)

def main():
    global segment
    try:
        with open(settings.streamDataPath(OS), "r") as f: # streamdata.json 読み込み
            streamdata = json.load(f)

        channelKeys = list(streamdata.keys()) # Channel Id リスト

        # Channel Id 2分割
        #（Twitterが凍結する可能性があるので2分割で時間を空けてチェックする）
        if 0 == segment:
            channelKeys = channelKeys[:int(len(list(streamdata.keys()))/2)]
            segment ^= 1 # 反転
        elif 1 == segment:
            channelKeys = channelKeys[int(len(list(streamdata.keys()))/2):]
            segment ^= 1

        for channelId in channelKeys:
            now = datetime.datetime.now()
            usrRoot = streamdata[channelId]
            if usrRoot['active_badge']: # Active Badge が有効なアカウントの場合
                try:
                    print(usrRoot["userName"]) # ユーザー名表示
                    userStatus = api.get_user(screen_name=usrRoot["twitterId"]) # ユーザー情報取得
                    photo = userStatus.profile_image_url_https
                    photo = photo.replace("_normal.jpg", "_400x400.jpg").replace("_normal.png", "_400x400.png")

                    if photo != usrRoot["photo"]:
                        usrRoot['photo'] = photo        # アイコン更新
                        usrRoot['iconUpdateCount'] += 1 # アップデート回数更新
                        usrRoot['lastIconUpdateDate'] = now.strftime("%Y/%m/%d %H:%M:%S") # 最終アイコンアップデート日更新
                        
                        writeLog('message', f'{usrRoot["userName"]}さんのアイコンデータを更新しました.\n')
                        print(usrRoot["userName"]+"さんのアイコンデータを更新しました.")

                except Exception as e:
                    if "User not found" in str(e): # Twitterアカウントが見つからなかった場合
                        writeLog('message', f'\"{channelId}\" {usrRoot["userName"]}さんのTwitterのアカウントが見つかりませんでした.\n')

                        twitterId = tui.searchTwitterId(usrRoot["twitterUserId"]) # ユーザーIDからTwitterIDを検索

                        # twitterIdの取得に成功したかどうか
                        if twitterId:
                            writeLog('message', f'{twitterId} TwitterIdの取得に成功しました.\n')
                            print(twitterId,"TwitterIdの取得に成功しました.")
                            usrRoot['twitterId'] = twitterId                # TwitterIDを更新
                        else:
                            writeLog('message', f'{usrRoot["twitterId"]} アカウントが削除されました.\n')
                            print(usrRoot["twitterId"], "アカウントが削除されました.")

                    elif "Invalid expired token" in str(e):
                        writeLog('error', "トークンが失効しました. トークンを更新してください.\n")

                    else:
                        writeLog('error', str(e)+"\n")
                sleep(1)
        return streamdata
        
    except Exception as e:
        print(str(e))
        open(".semaphore", "w").write("1")
        exit()

# スタートアップメッセージ
writeLog('message', '---- run updateTwitterIcon.py ----\n')

while True:
    # セマフォ確認
    while True:
        if "0" == open(".semaphore", "r").read():
            print("処理待機 60s...")
            sleep(60)
        else: break
    open(".semaphore", "w").write("0") # ブロック開始

    try:
        streamdata = main() # 更新したデータを返す
        with open(settings.streamDataPath(OS), "w") as f:
            json.dump(streamdata, f, indent=4) # 保存
        now = datetime.datetime.now()
        writeLog('message', 'アイコンアップデート完了.\n')

        open(".semaphore", "w").write("1") # ブロック終了

        print("待機中...")
        sleep(delay)
    except KeyboardInterrupt:
        print("キーが押されたので終了します.")
        open(".semaphore", "w").write("1")
        exit()