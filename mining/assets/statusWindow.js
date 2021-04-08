var ctx = document.getElementById("myChart");
var element_youtube = document.getElementById("youtube");
var element_statusWindow = document.getElementById("jquery-ui-draggable");
var element_mask = document.getElementById("mask");
var element_chatform = document.getElementById("chatform");
var e_underChatform = document.getElementById("underChatform");
var e_underChat = document.getElementById("underChat");
var e_underChatBtn = document.getElementById("underChatBtn");
var element_channelId = document.getElementById("channelId");
var element_userName = document.getElementById("userName");
var element_twitterId = document.getElementById("twitterId");
var element_videoTitle = document.getElementById("videoTitle");
var element_streamingNumber = document.getElementById("streamingNumber");
var element_livePoint = document.getElementById("livePoint");
var element_twitterId_link = document.getElementById("twitterId_link");
var element_youtubeId_link = document.getElementById("youtubeId_link");
var element_playgame = document.getElementById("playgame");
var element_playgame_link = document.getElementById("playgame_link");
var element_playgame_photo = document.getElementById("playgame_photo");
var videoId = "";

/* status window */
jQuery(function() { // element move draggable
    jQuery('#jquery-ui-draggable').draggable({
        handle: 'div'
    });
});

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
            backgroundColor: 'rgba(255, 98, 132, 0.5)',
            borderColor: 'rgba(255, 56, 99, 1)',
            borderWidth: 1
        }]
    }
});

var underChat_status = 0;

function status(channelId){
    // stop youtube interval
    clearInterval(yt_interval); // stop interval
    element_yt.setAttribute("src", "../startpage.html"); // set top page
    console.log("status "+channelId);
    element_mask.setAttribute("style", "display: block;"); // set mask
    element_statusWindow.setAttribute("style", ""); // status window on display
    
    for(let i=0;  i < streamings.length; i++){
        if(channelId == streamings[i]["channelId"]){
            videoId = streamings[i]["videoId"];
            element_channelId.innerText = channelId;
            element_userName.innerText = streamings[i]["userName"];
            element_twitterId.innerText = streamings[i]["twitterId"];
            element_videoTitle.innerText = streamings[i]["videoTitle"];
            element_streamingNumber.innerText = streamings[i]["streamingNumber"];
            element_livePoint.innerText = streamings[i]["livePoint"];
            if(streamings[i]["play"]){
                element_playgame.setAttribute("style", "display:block;width:100%;"); // playgame block
                element_playgame_link.setAttribute("href", streamings[i]["play"]["url"]);
                element_playgame_photo.setAttribute("src", streamings[i]["play"]["photo"]);
            }else{
                element_playgame.setAttribute("style", "display:none;width:100%;"); // playgame hidden
            }
            element_twitterId_link.setAttribute("href", "https://twitter.com/"+streamings[i]["twitterId"]);
            element_youtubeId_link.setAttribute("href", "https://www.youtube.com/watch?v="+videoId);
            // active chart
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
    // start youtube interval
    randomSetYouTube();
    yt_interval = setInterval(randomSetYouTube, speed);
    console.log("close status window.");
    element_mask.setAttribute("style", "display: none;"); // close mask
    element_statusWindow.setAttribute("style", "display: none;"); // close window
    element_chatform.setAttribute("src", ""); // close chat
    element_youtube.setAttribute("src", "https://www.youtube.com/embed/live_stream?channel=?"); // close youtube
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