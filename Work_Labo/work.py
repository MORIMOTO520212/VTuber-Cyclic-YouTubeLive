import json

with open('database/streamdata.json', 'r') as f:
    jsonData = json.load(f)

print(len(jsonData))