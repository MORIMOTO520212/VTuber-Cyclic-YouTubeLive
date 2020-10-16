<?php
# jsonファイルの内容を取得してその内容を返す #
# リンクはストレージサーバーにアクセス
function getStreaming() {
    return file_get_contents("http://f988ed573d32.ngrok.io/assets/streaming.json");
}
function getStreamData() {
    return file_get_contents("https://f988ed573d32.ngrok.io/database/streamdata.json");
}

if ( isset($_GET['mode']) ) {

    switch ($_GET['mode']) {
        case 'getStreaming':
            $data = getStreaming();
            break;
        case 'getStreamData':
            $data = getStreamData();
            break;
    }
    
    echo $data;
}
?>