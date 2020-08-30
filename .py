import json

with open("database/streamdata.json", "r") as f:
    data = json.load(f)

userName = []
for channelId in data:
        userName.append(data[channelId]["userName"])

input(userName)