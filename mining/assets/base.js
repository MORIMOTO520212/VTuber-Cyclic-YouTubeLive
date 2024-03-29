/* * * * * * * * * * * * * * * * * * *

    VTuber 採掘所 
    create: 2021/02/28
    update: 2021/08/23
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
var streamingChannel = "";

var element_yt              = document.getElementById("yt");
var element_main_userName   = document.getElementById("main_userName");
var element_main_videoTitle = document.getElementById("main_videoTitle");
var element_photo           = document.getElementById("photo");
var element_speed           = document.getElementById("speed");
var e_counter               = document.getElementById("counter");
var e_title                 = document.querySelector("title");
var streamings;
var streamDataCheck = false;
var _chlog = 0;
function intervalStreamingData(){
    function StreamingData(jsonData){
        streamings = jsonData;
        streamDataCheck = true;
        if(_chlog != streamings.length){
            liverViewer("", false); // update liver viewer
            gameFilter();  // update play games list
            e_counter.innerText = streamings.length;
            e_title.innerText = `VTuber採掘所 (${streamings.length})`;
            _chlog = streamings.length;
        }
    }
    $.post('../getData.php?mode=getStreaming', {}, function(data){
        console.log("getStreaming");
        jsonData = JSON.parse(data);
        StreamingData(jsonData);
    });
}
intervalStreamingData(); // get streaming data at intervals
setInterval(intervalStreamingData, 60000);



function randomSetYouTube(){
    console.log("randomSetYouTube");

    if (i < streamings.length-1){ i += 1; }
    else{ i = 0; }

    curtainOC(); // close curtain

    function sleep1(){
        element_yt.setAttribute("src", "https://www.youtube.com/embed/live_stream?channel="+streamings[i]["channelId"]+"&autoplay=1&mute=1&controls=0&modestbranding=0&showinfo=0");

        console.log("Channel ID: "+streamings[i]["channelId"]);
        streamingChannel                   = streamings[i]["channelId"];
        element_main_videoTitle.innerHTML  = streamings[i]["videoTitle"];        // メイン画面の動画タイトル
        element_main_userName.innerHTML    = "undefined";                        // ~ 初期設定 ~
        element_main_userName.innerHTML    = streamings[i]["userName"];          // メイン画面のユーザー名
        element_photo.setAttribute("src", streamings[i]["photo"]);               // メイン画面のTwitterアイコン

        let videoId = streamings[i]["videoId"];

    }
    setTimeout(sleep1, 1000); // 切り替え1秒前に幕を掛ける

    function sleep2(){
        curtainOC(); // open curtain
    }
    setTimeout(sleep2, 4500); // 幕を掛ける時間4.5秒
}


/* YouTube Player API */
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
        let wait=setInterval(function(){ // streamingが取得できるまで待機
            if(streamDataCheck){
                clearInterval(wait);
            }
        }, 500);
    }
}

var yt_interval;
var playStatus;
var speed = 30000; // YouTube Cyclic Speed | initial: 30s
function streaming(){
    playStatus = true;
    
    // YouTube画面に切り替え
    element_yt.setAttribute("style", "opacity: 1;");
    
    randomSetYouTube();
    yt_interval = setInterval(randomSetYouTube, speed);
}

function changeSpeed(){ // (int)seconds
    speed = element_speed.value*60000;
    console.log("changeSpeed "+speed);
    if(playStatus){
        clearInterval(yt_interval);
        yt_interval = setInterval(randomSetYouTube, speed);
    }
}


function streamStop(){
    clearInterval(yt_interval);
}

var sti;
function streamInterval(){
    if(streamDataCheck){
        streaming();
        console.log("Streaming start.");
        clearInterval(sti);
    }
}
sti = setInterval(streamInterval, 500);