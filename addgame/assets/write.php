<?php
# control.jsからjson XHR受信
$json_string = file_get_contents('php://input'); //  php://input は、POST の生データの読み込みを 許可します。
$data = json_decode($json_string);
var_dump($data);

?>