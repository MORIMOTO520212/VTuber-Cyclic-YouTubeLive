/* * * * * * * * * * * * * * * * * * *

    VTuber Cyclic Live Streaming 
    create: 2020/10/13
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
var element_streamingId = document.getElementById("streamingId");
var element_streamings  = document.getElementById("streamings");
var element_channelId   = document.getElementById("channelId");
var element_userName    = document.getElementById("userName");
var element_videoTitle  = document.getElementById("videoTitle");
var element_twitterId   = document.getElementById("twitterId");
var element_streamingNumber = document.getElementById("streamingNumber");
var element_main_userName   = document.getElementById("main_userName");
var element_main_videoTitle = document.getElementById("main_videoTitle");
var element_photo     = document.getElementById("photo");
var element_livePoint = document.getElementById("livePoint");
var element_play      = document.getElementById("play");
var element_speed     = document.getElementById("speed");
var element_playgame_photo  = document.getElementById("playgame_photo");
var element_playgame_link   = document.getElementById("playgame_link");
var ctx = document.getElementById("myChart");
var element_chatplay = document.getElementById("chatplay");
var element_chatform = document.getElementById("jquery-ui-draggable");
var element_chatformbtn = document.getElementById("chatformbtn");

var streamings;
function intervalStreamingData(){
    function StreamingData(jsonData){
        streamings = jsonData;
        var imgSource = "";
        for(var j = 0; j < streamings.length; j++){
            
            if(streamingChannel != streamings[j]["channelId"]){
                imgSource +=  "<a href=\"https://www.youtube.com/channel/"+streamings[j]["channelId"]+"\" target=\"_blank\"><img class=\"icon\" src=\"" + streamings[j]["photo"] + "\"></a>";
            
            }else{
                imgSource +=  "<a href=\"https://www.youtube.com/channel/"+streamings[j]["channelId"]+"\" target=\"_blank\"><img class=\"icon hilight\" src=\"" + streamings[j]["photo"] + "\"></a>";
            }
        }
        element_streamings.innerHTML = imgSource;        
    }
    $.post('getData.php?mode=getStreaming', {}, function(data){
        console.log("getStreaming");
        jsonData = JSON.parse(data);
        StreamingData(jsonData);
    });
}
intervalStreamingData();
setInterval(intervalStreamingData, 5000);

var chart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: [
            "00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", 
            "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"
        ],
        datasets: [{
            label: 'ライブポイント',
            data: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255,99,132,1)',
            borderWidth: 1
        }]
    }
});

var chatlist = [];
var lastmessageDate = 0; // 最新チャット時間
var videoId;
var chatStatus = false; // チャットオンオフ
var chatformStatus = false; // チャット欄オンオフ
var si_ca;
function StreamingChatData(liveChatData){ // チャットをchatlistに格納
    console.log("StreamingChatData");
    var items = liveChatData["items"];
    var item_length = liveChatData["items"].length;
    console.log("item length: "+item_length);
    for(var i = 0; i < item_length; i++){
        var messageDate = new Date(items[i]["snippet"]["publishedAt"]).getTime(); // 時刻取得
        if(lastmessageDate < messageDate){ // 時刻を比較して最新のチャットに絞る
            var message = items[i]["snippet"]["displayMessage"];  // メッセージ
            chatlist.push(message);
            lastmessageDate = messageDate;
        }
    }

    // 弾幕開始
    console.log("chat play");
    var i = 0;
    function chatAnimation(){
        //console.log("chat: "+chatlist[i]);
        $('#screen').comment(chatlist[i]); // チャットをコミット
        i++;
        if(0 == chatlist.length){  // チャンネルが切り替わったら終了
            clearInterval(si_ca);
            console.log("clearInterval - channel change");
        };   
        if(i == chatlist.length){ // チャットが最後まで到達した場合
            clearInterval(si_ca);
            console.log("clearInterval - next chat");
            loadStreamingChatData(videoId);
        };
    }
    si_ca = setInterval(chatAnimation, 1000);  // 100msでチャットを流す 280コメントで28秒
}

// チャット読み込み
function loadStreamingChatData(videoId){
    chatlist = [];
    $.post('getChat.php?v='+videoId, {}, function(data){
        console.log("getStreamingChatData "+videoId);
        jsonData = JSON.parse(data);
        StreamingChatData(jsonData);
    });
}

function randomSetYouTube(){
    console.log("randomSetYouTube");

    if (i < streamings.length-1){ i += 1; }
    else{ i = 0; }

    curtainOC(); // 幕を閉じる
    console.log("stream: "+i);

    // 弾幕システム初期化
    chatlist = [];
    lastmessageDate = 0;
    clearInterval(si_ca);

    function sleep1(){
        element_youtube.setAttribute("src", "https://www.youtube.com/embed/live_stream?channel="+streamings[i]["channelId"]+"&enablejsapi=1");

        //element_streamingId.innerHTML      = i;                                // ステータス画面のストリーミング番号
        element_channelId.innerHTML        = streamings[i]["channelId"];         // ステータス画面のチャンネルID
        streamingChannel                   = streamings[i]["channelId"];
        console.log("Channel ID: "+streamings[i]["channelId"]);
        element_videoTitle.innerHTML       = streamings[i]["videoTitle"];        // ステータス画面の動画タイトル
        element_main_videoTitle.innerHTML  = streamings[i]["videoTitle"];        // メイン画面の動画タイトル
        element_streamingNumber.innerHTML  = streamings[i]["streamingNumber"];   // ステータス画面の同時接続者数
        element_userName.innerHTML         = "undefined";                        // ~ 初期設定 ~
        element_twitterId.innerHTML        = "undefined";                        // 見つからなかった場合はundefinedを表示する
        element_main_userName.innerHTML    = "undefined";                        //
        element_userName.innerHTML         = streamings[i]["userName"];          // ステータス画面のユーザー名
        element_twitterId.innerHTML        = streamings[i]["twitterId"];         // ステータス画面のTwitterID
        element_livePoint.innerHTML        = streamings[i]["livePoint"]+" P";    // ステータス画面のライブポイント
        element_main_userName.innerHTML    = streamings[i]["userName"];          // メイン画面のユーザー名
        element_photo.setAttribute("src", streamings[i]["photo"]);               // メイン画面のTwitterアイコン
        if(streamings[i]["play"]){
            element_playgame_photo.setAttribute("style", "opacity: 1;");
            element_playgame_photo.setAttribute("src", streamings[i]["play"]["photo"]);
            element_playgame_link.setAttribute("href", streamings[i]["play"]["url"]);
        }else{
            element_playgame_photo.setAttribute("style", "opacity: 0;");
        }

        // アクティブ
        var activeStatus = streamings[i]["livePointStatus"];
        chart.data.datasets[0].data =   [
            activeStatus["00"], activeStatus["01"], activeStatus["02"], activeStatus["03"], 
            activeStatus["04"], activeStatus["05"], activeStatus["06"], activeStatus["07"],
            activeStatus["08"], activeStatus["09"], activeStatus["10"], activeStatus["11"], 
            activeStatus["12"], activeStatus["13"], activeStatus["14"], activeStatus["15"], 
            activeStatus["16"], activeStatus["17"], activeStatus["18"], activeStatus["19"], 
            activeStatus["20"], activeStatus["21"], activeStatus["22"], activeStatus["23"]
        ];
        chart.update();
        videoId = streamings[i]["videoId"];

        // チャット読み込み
        if(chatformStatus){
            domain = document.domain;
            url = "https://www.youtube.com/live_chat?v="+videoId+"&embed_domain="+domain;
            element_chatform.innerHTML = "<div class=\"ui-widget-header\"></div><iframe class=\"ui-widget-header\" frameborder=\"0\" src=\""+url+"\" allowfullscreen></iframe>";
        }
    }
    setTimeout(sleep1, 1000); // 切り替え1秒前に幕を掛ける

    function sleep2(){
        curtainOC(); // 幕を開ける
    }
    setTimeout(sleep2, 4500); // 幕を掛ける時間4.5秒

    // コメント読み込み chatStatus - True 再生 False 停止
    if(chatStatus){
        loadStreamingChatData(videoId);
    }
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
var apiCheck = false;
function onPlayerReady(event) {
    console.log("onPlayerReady");
    event.target.playVideo();
}
function onPlayerStateChange(event) {
    console.log("onPlayerStateChange "+event.data);
    apiCheck = true;
}

var interval;
var playStatus;
var speed = 60000; // 初期値60秒
function streaming(){
    if(apiCheck){
        playStatus = true;
        element_play.setAttribute("class", "play close");
    
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

function chatPlay(){
    if(chatStatus){
        // 停止する
        chatStatus = false;
        window.chatlist = [];
        lastmessageDate = 0;
        element_chatplay.innerText = "コメントを開始する";
    }else{
        // 開始する
        chatStatus = true;
        element_chatplay.innerText = "コメントを非表示にする";
    }
}

/* チャットドラッグ移動 */
jQuery(function() {
    jQuery('#jquery-ui-draggable').draggable({
        handle: 'div'
    });
});
/* 初期設定 チャットフォームを消す */
element_chatform.setAttribute("style", "position:relative; width:0; height:0;");
function chatform(){
    if(chatformStatus){
        // 停止する
        chatformStatus = false;
        element_chatformbtn.innerText = "チャットを表示する";
        element_chatform.innerHTML = "";
        element_chatform.setAttribute("style", "position:relative; width:0; height:0;");

    }else{
        // 開始する
        chatformStatus = true;
        element_chatformbtn.innerText = "チャットを非表示にする";
        element_chatform.setAttribute("style", "position:relative;");
        domain = document.domain;
        url = "https://www.youtube.com/live_chat?v="+videoId+"&embed_domain="+domain;
        element_chatform.innerHTML = "<div class=\"ui-widget-header\"></div><iframe class=\"ui-widget-header\" frameborder=\"0\" src=\""+url+"\" allowfullscreen></iframe>";
    }
}