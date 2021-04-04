import json, settings

with open(settings.streamDataPath("windows"), "r") as f:
    streamdata = json.load(f)

livePointStatus = []
for userdata in streamdata.values():
    lps = []
    for point in userdata["livePointStatus"].values():
        lps.append(point)
    print(lps)
    livePointStatus.append(lps)


for lps in livePointStatus:
    row = ""
    for point in lps:
        row += f"{point},"
    print(row)