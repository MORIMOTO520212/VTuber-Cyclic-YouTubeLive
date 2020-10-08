<?php
# jsonファイルの内容を取得してその内容を返す #
function getStreaming() {
    return file_get_contents("https://9d11a7fb872b.ngrok.io/assets/streaming.json");
}
function getStreamData() {
    return file_get_contents("https://9d11a7fb872b.ngrok.io/database/streamdata.json");
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