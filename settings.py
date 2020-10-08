# 設定

# ストリームデータの場所
def streamDataPath():
    return "/var/www/html/database/streamdata.json"
    #return "database/streamdata.json" windows

# ストリーミングデータの場所
def streamingDataPath():
    return "/var/www/html/assets/streaming.json"
    #return "assets/streaming.json" windows

# ユーザーID変換データの場所
def idChangeDataPath():
    return "/var/www/html/database/idChangeData.json"
    #return "database/idChangeData.json" windows

# Chromeのプロファイルの場所
def chromeProfilePath():
    return "C:\\Users\\kante\\AppData\\Local\\Google\\Chrome\\User Data2"

# Firefoxのプロファイルの場所
def firefoxProfilePath():
    return "firefox-profile"
    #return "C:\\Users\\kante\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\testProfile" windows

# Firefoxブラウザーの場所
def firefoxBinaryPath():
    return "C:\\Program Files\\Mozilla Firefox\\firefox.exe"