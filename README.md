# VTuber Cyclic YouTubeLive

Vtuberのライブ配信を巡回しながらライブ配信します。

機能  
コメントの30%が特定のVTuber名になるとその配信に切り替わる。（2度続けて同じVTuberは配信しない）

外部設計  
使用言語：HTML, CSS

内部設計  
使用言語：JS, Python

ファイル説明  
index.html - ストリーミングファイル  
addStreamData.py - ライバーの情報（ユーザー名・Twitter IDなど）を手動で記録します。  
streamingSearch.py - 登録しているライバーのライブ配信をstreaming.jsonに記録します。3分ごとに更新します。ユーザープロファイルを使っています。  

assets/
control.js - index.htmlのjsファイルです。ストリームの操作を行っています。  
effect.css - index.htmlのスタイルシートです。  
streaming.json - ライブ配信中のチャンネルIDを配列で記録しています。  

database/
streamdata.json - ライバーの情報（ユーザー名・Twitter IDなど）が記録されています。

Chromeブラウザでは音声付き動画の自動再生が禁止されているのでサイトの設定から音声を自動から許可に変更してあげる。  
ユーザープロファイルはコピーしたものを使う。

ライブ配信埋め込み禁止ライバー一覧  
夜白藍　 UC3G9ynwAEyiZU-87j6PkQLQ  
藤咲柊華 UC4P6fOfiK1lOED8CHoT9suw  
ジーク   UClxLspCGOP9Fy5Dvd7Kc77Q  
