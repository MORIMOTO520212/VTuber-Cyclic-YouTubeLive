import datetime

now = datetime.datetime.now()

hour = str(now.hour)
if hour == "0": hour = "00"

print(hour)