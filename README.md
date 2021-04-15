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
使用言語：HTML5, CSS, JS, Python, PHP, JSON  

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

Album/ - 画像記録やOGP素材の画像があります。

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

dashboard/  
    index.html - サーバーの管理画面です。登録者情報の閲覧やゲーム追加、サーバーログの監視をすることができます。  
    assets/  
        base.js  
        control.js  
        stream-control.js  
        style.css  
        write.php  

mining/  
    index.html  
    assets/
        game.js  
        gameFilter.js  
        liver.js  
        statusWindow.js  
        style.css  
        m-style.css  

register/  
    index.html  

status/  
    index.html  
    assets/  
        base.js  
        effect.css  

Work_Labo/  
    work.md - 作業内容を記載する。  
    work.py - 作業用Pythonファイル。


### 気になるライバー
奈辺陽鹿 再生不可 連絡中  
YouTube:https://www.youtube.com/channel/UCunmKT34H-FRMKwmSpwKDBA  
Twitter:https://twitter.com/youka_nabe  
白夢レイン 準備中  
YouTube:https://www.youtube.com/channel/UCIoM9dnD47MpnzV3EqEbg_g  
Twitter:https://twitter.com/Rain_Hakumu  
妖鬼水晶 活動中  
YouTube:https://www.youtube.com/channel/UCrNekQmlZQSQhxjov1Jz5Yw  
Twitter:https://twitter.com/Suisyou_cha  
園原満琴 活動中  
YouTube:https://www.youtube.com/channel/UCtQcumufS2xj4nGzJl7BxIw  
Twitter:https://twitter.com/makoto_sono  
七瀬タク 連絡する  
YouTube:https://www.youtube.com/channel/UCiqHlJh_i0z3PUadvlcWpEg  
Twitter:https://twitter.com/7se_taku  
百世アソブ 連絡する　配信頻度：低  
YouTube:https://www.youtube.com/channel/UCxzjHuyG5kd56vMDtUWzKAw  
Twitter:https://twitter.com/Momose_Asobu  
切取せん 連絡する  
YouTube:https://www.youtube.com/channel/UCSkAoufyYzfqBDlYPqjh_7A  
Twitter:https://twitter.com/k1ri_sen  

# NOTE   
twitter DM -> 黄昏にゃこさんはチャンネル登録者数が1000人未満にもかかわらず、配信中の埋め込みが許可されている。  
VTuberギルド -> ライブ配信アドバイザリー  VTuberギルドに参加しているライバーのライブ配信を分析しアドバイスする。  
各ライバーのゲーム配信における”最高同時接続者数”を記録する。  
各ライバーの1週間のライブ配信数を記録する。  


# streamdata.json 修正



6時から23時までgoodそれ以外bad  
統計人数：8人  
深夜帯倍率：36.837 %  

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