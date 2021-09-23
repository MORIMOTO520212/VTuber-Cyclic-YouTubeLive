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

### 記録データ一覧
- streamdata.json
    - ユーザー名
    - Twitter ID
    - Twitter画像
    - 合計ライブポイント
    - 最終ライブ配信日
    - Twitterアイコン更新回数
    - Twitterアイコン更新日
    - 時間別平均ライブポイント（0～23時）
    - これまでに遊んだゲーム
        - 製品名
        - 公式サイトリンク
        - 製品画像
        - 最後に遊んだ日付
    - コラボデータ（YouTubeチャンネルリスト）
    - アクティブバッジ（Boolean値）

### 削除ユーザー
羽衣みらい
YouTube: https://www.youtube.com/channel/UCHQM4sdkSoszo0wlHhwM4Gg

### streamdata.json 修正


### NOTE   
VTuber採掘所でハイライト動画が再生されない
idChangeData.jsonを参照する場合、すべて大文字にして小文字大文字判別しない
twitter DM -> 黄昏にゃこさんはチャンネル登録者数が1000人未満にもかかわらず、配信中の埋め込みが許可されている。   
    恐らく皆さんも、エンコーダに張り付けるストリームキーを固定するために、  
    「前の設定でスケジュール」を利用していると思いますが、  
    その「前」が「埋め込み許可(オフ)」だと、その設定が継続されてしまっているのでは無いでしょうか？  
各ライバーのゲーム配信における”最高同時接続者数”を記録する。  
各ライバーの1週間のライブ配信数を記録する。  

・VTuber採掘所
    右側に日別・週別の最高視聴配信ランキングを表示する。
    時間別の配信頻度グラフを表示する。
    注目のVtuber
    フィルターをもう少し増やす


### 再生不可のご連絡
失礼します。
VTuber配信巡回ウェブアプリ公式です。
VTuber採掘所にご登録頂いてありがとうございます。
サイトに掲載するために以下にご協力ください。
YouTube配信時に埋め込み許可をオンにしていない配信者をサイトに掲載することがシステム上できないようになっています。
引き続き掲載する場合は、埋め込み許可をオンにしてください。（次回からは自動的にオンになります）

手順
YouTube Studio > 

### サーバー再稼働
自宅サーバーを立ち上げる  
Apache2立ち上げ  
screen -S ngrok  
ngrok http 80  
screen -S streamingSearchFirefox  
python3 streamingSearchFirefox.py  
screen -S updateTwitterIcon  
python3 updateTwitterIcon.py  
getData.phpのngrokアドレス更新  
GCP VMインスタンスを立ち上げる  
Apache2立ち上げ  
getData.phpの書き換え  
お名前ドットコムでDNS更新  

