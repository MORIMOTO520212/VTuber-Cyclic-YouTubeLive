# TwitterUserIdを登録する
from module import twitter_user_id as tui
import json

with open('database/streamdata.json', 'r') as f:
    streamData = json.load(f)

try:
    for channelId in streamData.keys():
        try: _tui = streamData[channelId]["twitterUserId"]
        except:
            twitterUserId = tui.getTwitterUserId(streamData[channelId]["twitterId"])
            print(streamData[channelId]["userName"], twitterUserId)
            if twitterUserId:
                streamData[channelId]["twitterUserId"] = twitterUserId
except KeyboardInterrupt:
    pass

with open('database/streamdata.json', 'w') as f:
    json.dump(streamData, f, indent=4)