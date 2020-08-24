<?php
# jsonファイルの内容を取得してその内容を返す #
function getStreaming() {
    return file_get_contents("assets/streaming.json");
}
function getStreamData() {
    return file_get_contents("database/streamdata.json");
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