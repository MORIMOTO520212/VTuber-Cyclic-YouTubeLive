<?php
# jsonファイルの内容を取得してその内容を返す #
# リンクはストレージサーバーにアクセス
$ngrok = "http://cc7670c936b4.ngrok.io";

function getStreaming() {
    global $ngrok;
    return file_get_contents($ngrok."/assets/streaming.json");
}
function getStreamData() {
    global $ngrok;
    return file_get_contents($ngrok."/database/streamdata.json");
}
function getGames_local() {
    return file_get_contents("database/games.json");
}

if ( isset($_GET['mode']) ) {

    switch ($_GET['mode']) {
        case 'getStreaming':
            $data = getStreaming();
            break;
        case 'getStreamData':
            $data = getStreamData();
            break;
        case 'getGames_local':
            $data = getGames_local();
    }
    
    echo $data;
}
?>