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
index.html - ストリーミングファイル  
streamtest.html - チャンネルが埋め込み許可をしているかどうかを調べます。  
startpage.html - index.htmlで使います。再生前の注意事項などを記載したファイルです。  
addStreamData.py - ライバーの情報（ユーザー名・Twitter IDなど）を手動で記録します。  
streamingSearchChrome.py - 登録しているライバーのライブ配信をstreaming.jsonに記録します。3分ごとに更新します。ユーザープロファイルを使っています。  
streamingSearchFirefox.py - 登録しているライバーのライブ配信をstreaming.jsonに記録します。3分ごとに更新します。こちらをメインで使ってください。  
getData.php - ファイルからデータを取得します。  
chromedriver.exe - streamingSearchChrome.pyでseleniumを使います。Chromeブラウザに合ったバージョンを使ってください。  
geckodriver.exe - streamingSearchFirefox.pyでseleniumを使います。  
setting.py - ファイルの場所などの設定が書かれているモジュールです。  

assets/  
control.js - index.htmlのjsファイルです。ストリームの操作を行っています。  
effect.css - index.htmlのスタイルシートです。  
streaming.json - ライブ配信中のチャンネルIDを配列で記録しています。  

database/  
streamdata.json - ライバーの情報（ユーザー名・Twitter IDなど）が記録されています。  
idChangeData.json - スクレイピングでユーザーIDで取得された場合にチャンネルIDに変更します。
guide.mp4 - index.htmlで使うファイルです。  

about/
usage/
vtuber/
bugreport/

画質が落ちた場合、現在このサイトは画質変更機能がないのでYouTubeにアクセスし画質を戻してからこのサイトに戻ってください。

### 未登録ライバー


### 未登録ゲーム 

NOTE
ライブ配信のタイトルに他のライバー名が入っている場合記録し、コラボ状況を調査  


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