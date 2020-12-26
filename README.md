# VTuber Cyclic YouTubeLive

### Vtuberのライブ配信を巡回しながらライブ配信します。  

### 開発環境
Windows10  
Linux  

### 仕組み
GCPでサイトを公開し、データは自宅のストレージサーバーで管理。

### 機能  
ウェブアプリ化  
ライブポイント（3分間ごとに1ポイント加える）  
アクティブ（ライブポイントと時間帯）  
最終ライブ配信日  
アイコン更新回数  
最終アイコン更新日  
長時間配信者はアイコンの位置が上に来ます  
ライブ配信化 - コメントの30%が特定のVTuber名になるとその配信に切り替わる。（2度続けて同じVTuberは配信しない）  
↑まだ実装予定なし  

### 外部設計  
使用言語：HTML, CSS  

### 内部設計  
使用言語：JS, Python, PHP  

### ファイル説明  
.semaphore - streamdata.jsonの排他制御を行います。これはstreamingSearchFirefox.pyとupdateTwitterIcon.pyが利用します。
index.html - ストリーミングファイル  
streamtest.html - チャンネルが埋め込み許可をしているかどうかを調べます。  
startpage.html - index.htmlで使います。再生前の注意事項などを記載したファイルです。  
addStreamData.py - ライバーの情報（ユーザー名・Twitter IDなど）を手動で記録します。  
streamingSearchChrome.py - 登録しているライバーのライブ配信をstreaming.jsonに記録します。3分ごとに更新します。ユーザープロファイルを使っています。  
streamingSearchFirefox.py - 登録しているライバーのライブ配信をstreaming.jsonに記録します。3分ごとに更新します。こちらをメインで使ってください。  
getData.php - streaming.json, streamdata.jsonからデータを取得します。 
getChat.php - YouTube Data API v3からライブ配信のチャットを取得する。
chromedriver.exe - streamingSearchChrome.pyでseleniumを使います。Chromeブラウザに合ったバージョンを使ってください。  
geckodriver.exe - streamingSearchFirefox.pyでseleniumを使います。  
setting.py - ファイルの場所などの設定が書かれているモジュールです。  
requirements.txt - Pythonのプログラムで使うモジュールをまとめたファイルです。
channels.txt - addStreamData.pyで一括でファイルを追加するためのテキストファイルです。
YouTubeDataAPI_liveChat.json - YouTubeData API v3で取得したチャットを記録する。サンプルファイルなので他のプログラムには直結しない。
dbAdd.py - 既存のstreamdata.jsonに新しく追加するキーを全てに適応するためのプログラム。

assets/  
    control.js - index.htmlのjsファイルです。ストリームの操作を行っています。  
    effect.css - index.htmlのスタイルシートです。  
    streaming.json - ライブ配信中のチャンネルIDを配列で記録しています。  
    nncomment.js - ニコニコ弾幕の再現ソースコード　開発者：https://github.com/wmoai/jquery.nncomment

database/  
    streamdata.json - ライバーの情報（ユーザー名・Twitter IDなど）が記録されています。  
    idChangeData.json - スクレイピングでユーザーIDで取得された場合にチャンネルIDに変更します。  
    games.json - ゲーム配信中にゲームを検出するために使うデータファイルです。

about/  
    index.html - このサイトについての情報が書かれている。  
    style.css  - index.htmlのスタイル  

addgame/
    index.html - games.jsonにゲーム情報を登録するためのサイトです。
    assets/
        control.js - index.htmlで使うファイルで、データの整理をしています。
        style.css - index.htmlのスタイルシートです。
        write.php - control.jsから送られたjson情報をgames.jsonに上書きします。

usage/  
    index.html - このサイトの使い方について書かれている。  
    style.css  - index.htmlのスタイル  

vtuber/  
    index.html - このサイトに登録しているVTuberについて書かれている。  
    style.css  - index.htmlのスタイル  

bugreport/  
    index.html - このサイトのバグについて書かれている。  
    style.css  - index.htmlのスタイル  

collabnetwork/  
    index.html - コラボ状況について書かれている。
    assets/ network.js - コラボ状況の操作  
    assets/ style.css  - index.htmlのスタイル  

画質が落ちた場合、現在このサイトは画質変更機能がないのでYouTubeにアクセスし画質を戻してからこのサイトに戻ってください。

### 気になるライバー
真神ラフィ 埋め込み禁止中
YouTube:https://www.youtube.com/channel/UCBaSCYQid-__CE6bnUPWXrw  
Twitter:https://twitter.com/maga3_raffi  
白夢レイン 準備中
Twitter:https://twitter.com/Rain_Hakumu
妖鬼水晶 準備中
YouTube:https://www.youtube.com/channel/UCrNekQmlZQSQhxjov1Jz5Yw
Twitter:https://twitter.com/Suisyou_cha
園原満琴 準備中
YouTube:https://www.youtube.com/channel/UCtQcumufS2xj4nGzJl7BxIw
Twitter:https://twitter.com/makoto_sono

NOTE  


データを一部だけ変更するプログラムの作成
6時から23時までgoodそれ以外bad  
統計人数：8人  
深夜帯倍率：36.83686608469389 %  

good 1087  bad 157  
good 1281  bad 467  
good 188   bad 73  
good 614   bad 170  
good 245   bad 116  
good 476   bad 168  
good 1349  bad 193  
good 605   bad 486  

※倍率は高い方が健康  
健康倍率：(good ÷ bad)の総和 ÷ サンプルサイズ  

※健康度がプラスになれば健康、マイナスなら不健康  
健康度：(good ÷ bad) - 健康倍率   


ch1 - [ch2,ch3,ch4]
ch2 - [ch1,ch3,ch6]
ch3 - [ch1,ch2,ch5]
ch4 - [ch1,ch3,ch5]
ch5 - [ch3,ch4]
ch6 - [ch2]

channel = GET data.json
already = []
edges = []
for channel {
    check = true
    for already {
        if channel == already {
            check = false
        }
    }
    if check {
        edges append {from ch to ch}
    }
}

json
"collab": ["channelId","channelId"]