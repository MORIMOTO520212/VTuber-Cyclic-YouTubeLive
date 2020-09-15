# VTuber Cyclic YouTubeLive

## Vtuberのライブ配信を巡回しながらライブ配信します。  

### 機能  
コメントの30%が特定のVTuber名になるとその配信に切り替わる。（2度続けて同じVTuberは配信しない）  
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
streamingSearch.py - 登録しているライバーのライブ配信をstreaming.jsonに記録します。3分ごとに更新します。ユーザープロファイルを使っています。  
getData.php - ファイルからデータを取得します。
chromedriver.exe - streamingSearch.pyでseleniumを使います。Chromeブラウザに合ったバージョンを使ってください。  

assets/
control.js - index.htmlのjsファイルです。ストリームの操作を行っています。  
effect.css - index.htmlのスタイルシートです。  
streaming.json - ライブ配信中のチャンネルIDを配列で記録しています。  

database/
streamdata.json - ライバーの情報（ユーザー名・Twitter IDなど）が記録されています。
guide.mp4 - index.htmlで使うファイルです。

Chromeブラウザでは音声付き動画の自動再生が禁止されているのでサイトの設定から音声を自動から許可に変更してあげる。  
ユーザープロファイルはコピーしたものを使う。
OBSでソースにブラウザを設定し、altキーを押しながらクロップ（トリミング）を行う。

### ライブ配信埋め込み禁止ライバー一覧  
夜白藍      UC3G9ynwAEyiZU-87j6PkQLQ  
藤咲柊華    UC4P6fOfiK1lOED8CHoT9suw  
ジーク      UClxLspCGOP9Fy5Dvd7Kc77Q  
錫白レイ    UCuzEiEIsbACj56uLxxd-5Vw  
星名レキ    UCQCJfZ3ClRFkf2Pgy5n2_NA  
香月ネロ    UCrKFWIOpVNwpyzfoTH0w6bQ  
音無ツバキ  UC6USecxNGku4qbOAa6hF1rA  
桔梗ちはる  UCf6REJh1e1YUyYPKmDaz8Ig  
ユノ        UC0OxbHy1_rtjTk946-hWTnA  
戸越ぷらむ  UCk7cMvrfvH98Bfng58N_Zzw  
塩天使リエル UCE5rWcDxLPaaUFWOxzJFfNg  
夜野とばり  UC2JMXD8btPtvJafM3dawF-Q  
碧那アイル  UCpBCiBjOoZanFhj-49LgcDg  
アイリス・ヴェール UCqo0CAZ46l6ic3A_LfhEgHg  