import json

with open('database/streamdata.json', 'r') as f:
    streamData = json.load(f)

with open('Work_labo/channelId.txt', 'r') as f:
    del_channelId = f.readlines()

for channelId in del_channelId:
    channelId = channelId.replace("\n", "")
    del streamData[channelId]

with open('database/streamdata.json', 'w') as f:
    json.dump(streamData, f, indent=4)