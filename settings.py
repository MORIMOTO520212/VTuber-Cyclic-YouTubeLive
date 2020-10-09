# 設定

# ストリームデータの場所
def streamDataPath(os):
    if os == "windows":
        return "database/streamdata.json"
    if os == "linux":
        return "/var/www/html/database/streamdata.json"
    return False

# ストリーミングデータの場所
def streamingDataPath(os):
    if os == "windows":
        return "assets/streaming.json"
    if os == "linux":
        return "/var/www/html/assets/streaming.json"
    return False

# ユーザーID変換データの場所
def idChangeDataPath(os):
    if os == "windows":
        return "database/idChangeData.json"
    if os == "linux":
        return "/var/www/html/database/idChangeData.json"
    return False

# Chromeのプロファイルの場所
def chromeProfilePath(os):
    if os == "windows":
        return "C:\\Users\\kante\\AppData\\Local\\Google\\Chrome\\User Data2"
    if os == "linux":
        return ""
    return False

# Firefoxのプロファイルの場所
def firefoxProfilePath(os):
    if os == "windows":
        return "C:\\Users\\kante\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\testProfile"
    if os == "linux":
        return "firefox-profile"
    return False

# Firefoxブラウザーの場所
def firefoxBinaryPath(os):
    if os == "windows":
        return "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
    if os == "linux":
        return ""
    return False