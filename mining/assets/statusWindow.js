var ctx                = document.getElementById("myChart");
var element_youtube      = document.getElementById("youtube");
var element_statusWindow = document.getElementById("jquery-ui-draggable");
var element_mask       = document.getElementById("mask");
var element_chatform   = document.getElementById("chatform");
var e_underChatform    = document.getElementById("underChatform");
var e_underChat        = document.getElementById("underChat");
var e_underChatBtn     = document.getElementById("underChatBtn");
var element_channelId  = document.getElementById("channelId");
var element_channellnk = document.getElementById("channellnk");
var element_userName   = document.getElementById("userName");
var element_twitterId  = document.getElementById("twitterId");
var element_twitterlnk = document.getElementById("twitterlnk");
var element_videoTitle = document.getElementById("videoTitle");
var element_streamingNumber = document.getElementById("streamingNumber");
var element_livePoint       = document.getElementById("livePoint");
var element_playgame        = document.getElementById("playgame");
var element_playgame_link   = document.getElementById("playgame_link");
var element_playgame_photo  = document.getElementById("playgame_photo");
var element_liveStartTime   = document.getElementById("liveStartTime");
var videoId = "";


var chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [
            "00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", 
            "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"
        ],
        datasets: [{
            label: '配信頻度',
            data: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            borderColor: 'rgba(255, 56, 99, 1)',
            backgroundColor: 'rgba(255, 98, 132, 0.5)',
            fill: true,
            borderWidth: 1
        }]
    }
});

var underChat_status = 0;

function status(channelId){
    // バックグラウンド画面の配信を停止
    clearInterval(yt_interval);
    element_yt.setAttribute("src", "../startpage.html");
    console.log("status "+channelId);

    // StatusWindowの表示
    element_mask.setAttribute("style", "display: block;"); // 画面にマスク
    element_statusWindow.setAttribute("style", "");
    
    // StatusWindowの内容を表示
    for(let i=0;  i < streamings.length; i++){
        if(channelId == streamings[i]["channelId"]){
            videoId = streamings[i]["videoId"];

            // チャンネル ID
            element_channelId.innerText = channelId;
            element_channellnk.setAttribute('href', 'https://www.youtube.com/channel/'+channelId);
            // 動画タイトル
            element_videoTitle.innerText = streamings[i]["videoTitle"];
            // ユーザー名
            element_userName.innerText = streamings[i]["userName"];
            // Twitter ID
            element_twitterId.innerText = streamings[i]["twitterId"];
            element_twitterlnk.setAttribute('href', 'https://twitter.com/'+streamings[i]["twitterId"]);
            // 同時接続者数
            element_streamingNumber.innerText = streamings[i]["streamingNumber"];
            // ライブポイント
            element_livePoint.innerText = streamings[i]["livePoint"];
            // 配信開始（年はsliceで削った）
            element_liveStartTime.innerText = streamings[i]["liveStartTime"].slice(5);
            // プレイ中のゲーム
            if(streamings[i]["play"]){
                element_playgame.setAttribute("style", "display:block;width:100%;");
                element_playgame_link.setAttribute("href", streamings[i]["play"]["url"]);
                element_playgame_photo.setAttribute("src", streamings[i]["play"]["photo"]);
            }else{
                element_playgame.setAttribute("style", "display:none;width:100%;");
            }

            // アクティブチャート
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
        }
    }
    let domain = document.domain;
    let chat_url = "https://www.youtube.com/live_chat?v="+videoId+"&embed_domain="+domain;
    element_chatform.setAttribute("src", chat_url);
    element_youtube.setAttribute("src", "https://www.youtube.com/embed/live_stream?channel="+channelId+"&enablejsapi=1");
}

function closeStatusWindow(){
    // バックグラウンド画面の配信を開始
    randomSetYouTube();
    yt_interval = setInterval(randomSetYouTube, speed);
    console.log("close status window.");
    element_mask.setAttribute("style", "display: none;"); // close mask
    element_statusWindow.setAttribute("style", "display: none;"); // close window
    element_chatform.setAttribute("src", ""); // close chat
    element_youtube.setAttribute("src", "https://www.youtube.com/embed/live_stream?channel=?"); // close youtube
    // close chat
    e_underChat.setAttribute("style", "display:none");
    e_underChatform.setAttribute("src", "");
    e_underChatBtn.innerText = "チャット欄を表示";
    underChat_status = 0; // close under chat
}


function underChatform(){
    if(!underChat_status){
        console.log("under chat form.")
        let domain = document.domain;
        let chat_url = "https://www.youtube.com/live_chat?v="+videoId+"&embed_domain="+domain;
        e_underChat.setAttribute("style", "display:block");
        e_underChatform.setAttribute("src", chat_url);
        e_underChatBtn.innerText = "チャット欄を非表示";
        underChat_status = 1; // display under chat
    }else{
        e_underChat.setAttribute("style", "display:none");
        e_underChatform.setAttribute("src", "");
        e_underChatBtn.innerText = "チャット欄を表示";
        underChat_status = 0; // close under chat
    }
}