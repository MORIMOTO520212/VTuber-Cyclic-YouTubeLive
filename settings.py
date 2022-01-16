# 設定
# osごとにファイルの場所を一括変更するためのモジュールファイルです。
# 各自の環境に合わせてパスを設定して下さい。

# ストリームデータの場所
def streamDataPath(os):
    'streamDataPath(str) <- windows, linux'
    if os == "windows":
        return "database/streamdata.json"
    if os == "linux":
        return "/var/www/html/database/streamdata.json"
    return "false"

# ストリーミングデータの場所
def streamingDataPath(os):
    'streamingDataPath(str) <- windows, linux'
    if os == "windows":
        return "assets/streaming.json"
    if os == "linux":
        return "/var/www/html/assets/streaming.json"
    return "false"

# ユーザーID変換データの場所
def idChangeDataPath(os):
    'idChangeDataPath(str) <- windows, linux'
    if os == "windows":
        return "database/idChangeData.json"
    if os == "linux":
        return "/var/www/html/database/idChangeData.json"
    return "false"

# メッセージログの場所
def messageLogPath(os):
    'messageLogPath(str) <- `windows`, `linux`'
    if os == "windows":
        return "message.log"
    if os == "linux":
        return "/var/www/html/log/message.log"
    return "false"

# エラーログの場所
def errorLogPath(os):
    'errorLogPath(str) <- `windows`, `linux`'
    if os == "windows":
        return "error.log"
    if os == "linux":
        return "/var/www/html/log/error.log"
    return "false"

# ストリーミングログの場所
def streamingLogPath(os):
    'streamingLogPath(str) <- `windows`, `linux`'
    if os == "windows":
        return "log/streaming"
    if os == "linux":
        return "/var/www/html/log/streaming"
    return "false"

# Chromeのプロファイルの場所（streamingSearchChrome.pyを使う場合）
def chromeProfilePath(os):
    'chromeProfilePath(str) <- `windows`, `linux`'
    if os == "windows":
        return "C:\\Users\\kante\\AppData\\Local\\Google\\Chrome\\User Data2"
    if os == "linux":
        return ""
    return "false"

# Firefoxのプロファイルの場所
def firefoxProfilePath(os):
    'firefoxProfilePath(str) <- `windows`, `linux`'
    if os == "windows":
        return "C:\\Users\\kante\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\5vq40w5z.default-esr"
    if os == "linux":
        return "firefox-profile"
    return "false"

# Firefoxブラウザーの場所
def firefoxBinaryPath(os):
    'firefoxBinaryPath(str) <- windows, linux'
    if os == "windows":
        return "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
    if os == "linux":
        return ""
    return "false"

# ゲームデータの場所
def gamesDataPath(os):
    'gamesDataPath(str) <- windows, linux'
    if os == "windows":
        return "database/games.json"
    if os == "linux":
        return "/var/www/html/database/games.json"
    return "false"

# Tweepy
def tweepyKeyPath():
    consumer_key    = 'fOr1fbI9mCK1ztiqbEIMlHfLV'
    consumer_secret = 'PdVL9Fb166jY7VMjXuA8EkjN4mWNlkEFI6XT3mTIEbqkVDGwMb'
    access_key      = '4634604300-uYOEizJIhTQWMan2pLtfK9r73nXK5BK0h4rlwf3'
    access_secret   = '54Dqdt8Kx7CoVKq2XqOSoTsKkTI7liPtpPugaZjGrTbRK'
    return consumer_key, consumer_secret, access_key, access_secret