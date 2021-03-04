/* * * * * * * * * * * * * * * * * * *

    VTuber 採掘所 
    create: 2021/02/28
    update: 2021/02/28
    GitHub:
    Twitter: @Medaka_bridle

* * * * * * * * * * * * * * * * * * */

function curtainOC(){
    element_curtain = document.getElementById("curtain");
    if(element_curtain.className == "curtain open"){
        element_curtain.className = "curtain close";
        console.log("curtain close");
    }else{
        element_curtain.className = "curtain open";
        console.log("curtain open");
    }
    return;
}

var i = 0;
var streamingChannel    = "";

var element_youtube     = document.getElementById("youtube");
var element_startpage   = document.getElementById("startpage");
var element_main_userName   = document.getElementById("main_userName");
var element_main_videoTitle = document.getElementById("main_videoTitle");
var element_photo     = document.getElementById("photo");
var element_speed     = document.getElementById("speed");

var streamings;
var streamDataCheck = false;
function intervalStreamingData(){
    function StreamingData(jsonData){
        streamings = jsonData;
        streamDataCheck = true;     
    }
    $.post('../getData.php?mode=getStreaming', {}, function(data){
        console.log("getStreaming");
        jsonData = JSON.parse(data);
        StreamingData(jsonData);
    });
}
intervalStreamingData();
setInterval(intervalStreamingData, 5000);



function randomSetYouTube(){
    console.log("randomSetYouTube");

    if (i < streamings.length-1){ i += 1; }
    else{ i = 0; }

    curtainOC(); // 幕を閉じる
    console.log("stream: "+i);


    function sleep1(){
        element_youtube.setAttribute("src", "https://www.youtube.com/embed/live_stream?channel="+streamings[i]["channelId"]+"&enablejsapi=1&mute=1");

        streamingChannel                   = streamings[i]["channelId"];
        console.log("Channel ID: "+streamings[i]["channelId"]);
        element_main_videoTitle.innerHTML  = streamings[i]["videoTitle"];        // メイン画面の動画タイトル
        element_main_userName.innerHTML    = "undefined";                       // ~ 初期設定 ~
        element_main_userName.innerHTML    = streamings[i]["userName"];          // メイン画面のユーザー名
        element_photo.setAttribute("src", streamings[i]["photo"]);               // メイン画面のTwitterアイコン

        videoId = streamings[i]["videoId"];

    }
    setTimeout(sleep1, 1000); // 切り替え1秒前に幕を掛ける

    function sleep2(){
        curtainOC(); // 幕を開ける
    }
    setTimeout(sleep2, 4500); // 幕を掛ける時間4.5秒
}

var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;
function onYouTubeIframeAPIReady() {
    player = new YT.Player("youtube",{
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        }
    });
}
var _apiCheck = 0;
var apiCheck = false;
function onPlayerReady(event) {
    console.log("onPlayerReady");
    event.target.playVideo();
}
function onPlayerStateChange(event) {
    console.log("onPlayerStateChange "+event.data);
    if(-1 == event.data){
        _apiCheck++;
    }
    if(2 == _apiCheck){
        apiCheck = true;
        while(streamDataCheck){ // streamデータが取得できるまで待機
            console.log("Streaming start.");
            streaming();
            break;
        }
    }
}

var interval;
var playStatus;
var speed = 60000; // 初期値60秒
function streaming(){
    if(apiCheck){
        playStatus = true;
    
        // YouTube画面に切り替え
        element_startpage.setAttribute("style", "opacity: 0;");
        element_youtube.setAttribute("style", "opacity: 1;");
    
        randomSetYouTube();
        interval = setInterval(randomSetYouTube, speed);
    }else{
        alert("Opps!\nYouTube Player APIでエラーが発生しました。サイトをリロードします。");
        location.reload();
    }
}

function changeSpeed(){
    speed = element_speed.value*60000;
    console.log("changeSpeed "+speed);
    if(playStatus){
        clearInterval(interval);
        interval = setInterval(randomSetYouTube, speed);
    }
}


function streamStop(){
    clearInterval(interval);
}

/* status window */
jQuery(function() { // 要素ドラッグ移動
    jQuery('#jquery-ui-draggable').draggable({
        handle: 'div'
    });
});