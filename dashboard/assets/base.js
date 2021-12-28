var e_message_log = document.getElementById("message_log");
var e_error_log   = document.getElementById("error_log");

/* ログ取得 */
function messageLog(log){
    console.log("get message log.");
    e_message_log.innerText = "- message log -" + log;
}
function errorLog(log){
    console.log("get error log.");
    e_error_log.innerText = "- error log -" + log;
}
function intervalLog(){
    $.post('../getData.php?mode=message_log', {}, function(data){messageLog(data)});
    $.post('../getData.php?mode=error_log', {}, function(data){errorLog(data)});
    if(0 == e_message_log.scrollTop || e_message_log.scrollHeight == e_message_log.scrollTop) e_message_log.scrollTop = e_message_log.scrollHeight;
    if(0 == e_error_log.scrollTop || e_error_log.scrollHeight == e_error_log.scrollTop) e_error_log.scrollTop = e_error_log.scrollHeight;
}
intervalLog();
setInterval(intervalLog, 10000);