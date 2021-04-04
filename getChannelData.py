#   YouTube Data API
import requests, json

channelId = "UCZlDXzGoo7d44bwdNObFacg"

params = {"part": "statistics", "id": channelId, "key": "AIzaSyAqPZKM0ZwrZ6Xs4ZPae5Xx1jOfGaMmyS8"}

res = requests.get("https://www.googleapis.com/youtube/v3/channels", params=params)
channel = res.json()

subscriberCount = channel["items"][0]["statistics"]["subscriberCount"] # チャンネル登録者数
viewCount = channel["items"][0]["statistics"]["viewCount"] # 総視聴回数
videoCount = channel["items"][0]["statistics"]["videoCount"] # 投稿動画本数

print("チャンネル登録者数：", subscriberCount)
print("総視聴回数：", viewCount)
print("投稿動画本数：", videoCount)