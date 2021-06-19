<?php
# jsonファイルの内容を取得してその内容を返す #
# リンクはストレージサーバーにアクセス
$ngrok = "https://bece39171004.ngrok.io";

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
function message_log() {
    global $ngrok;
    return file_get_contents($ngrok."/log/message.log");
}
function error_message_log() {
    global $ngrok;
    return file_get_contents($ngrok."/log/error.log");
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
            break;
        case 'message_log':
            $data = message_log();
            break;
        case 'error_log':
            $data = error_message_log();
    }
    
    echo $data;
}
?>