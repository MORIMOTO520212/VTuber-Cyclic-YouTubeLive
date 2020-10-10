# VTuber Cyclic YouTubeLive

### Vtuberのライブ配信を巡回しながらライブ配信します。  

### 開発環境
Windows10  
Linux  

### 仕組み
レンタルサーバーでサイトを公開し、データの取得は自宅でストレージサーバーを立てる。

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

Chromeブラウザでは音声付き動画の自動再生が禁止されているのでサイトの設定から音声を自動から許可に変更してあげる。  
OBSでソースにブラウザを設定し、altキーを押しながらクロップ（トリミング）を行う。  

画質が落ちた場合、現在このサイトは画質変更機能がないのでYouTubeにアクセスし画質を戻してからこのサイトに戻ってください。

### 未登録ライバー
鳴蝶院アドニス
Adonis_AI_
UCVrD1IwbhqOshMSO0Q8Lqpw

えりるる
eriruru3
UCddl7tgJDy9uHoUJm7yH4Vw

loveちゃん
lovechan_lp
UCYm8zALd2uHqyy6C1tb4_zA


### 未登録ゲーム
Watch Dogs    
DARK SOULSⅡ  
DARK SOULSⅢ  
ゼルダの伝説  
スーパーマリオ64  

NOTE
ライブ配信のタイトルに他のライバー名が入っている場合記録し、コラボ状況を調査  