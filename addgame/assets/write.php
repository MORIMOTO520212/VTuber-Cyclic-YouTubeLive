<?php
# control.jsからjson XHR受信
$json_string = file_get_contents('php://input'); //  php://input は、POST の生データの読み込みを 許可します。
$json_string = mb_convert_encoding($json_string, 'UTF8', 'ASCII,JIS,UTF-8,EUC-JP,SJIS-WIN');
$games = json_decode($json_string);

file_put_contents("../../database/games.json", json_encode($games), LOCK_EX);

?>