<?php
# jsonファイルの内容を取得してその内容を返す #
# YouTubeData API v3 Live Chat

$key = "AIzaSyAqPZKM0ZwrZ6Xs4ZPae5Xx1jOfGaMmyS8";
$maxResults = "75"; # なぜか75に制限される。

function getchat($videoId) {
    global $key, $maxResults;
    $videos    = file_get_contents("https://www.googleapis.com/youtube/v3/videos?part=liveStreamingDetails&id=".$videoId."&key=".$key);
    $videos    = mb_convert_encoding($videos, 'UTF8', 'ASCII,JIS,UTF-8,EUC-JP,SJIS-WIN');
    $videoData = json_decode($videos, true);
    $activeLiveChatId = $videoData["items"][0]["liveStreamingDetails"]["activeLiveChatId"];
    return file_get_contents("https://www.googleapis.com/youtube/v3/liveChat/messages?liveChatId=".$activeLiveChatId."&part=authorDetails,snippet&hl=ja&maxResults=".$maxResults."&key=".$key);

}

function demo_getchat($videoId) {
    return file_get_contents("YouTubeDataAPI_liveChat.json");
}

if ( isset($_GET['v']) ) {
    $videoId = $_GET['v'];
    $data = getchat($videoId);
    echo $data;
}
if ( isset($_GET['demo']) ) {
    $videoId = $_GET['demo'];
    $data = demo_getchat($videoId);
    echo $data;
}
?>