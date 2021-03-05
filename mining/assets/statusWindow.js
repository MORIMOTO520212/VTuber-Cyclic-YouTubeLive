var element_statusWindow = document.getElementById("jquery-ui-draggable");
var element_mask = document.getElementById("mask");
var element_chatform = document.getElementById("chatform");

/* status window */
jQuery(function() { // 要素ドラッグ移動
    jQuery('#jquery-ui-draggable').draggable({
        handle: 'div'
    });
});

function status(channelId){
    clearInterval(yt_interval); // stop youtube interval
    console.log(channelId);
    element_mask.setAttribute("style", "display: block;");
    element_statusWindow.setAttribute("style", "");
    let videoId;
    for(let i=0;  i < streamings.length; i++){
        console.log(streamings[i]["channelId"]);
        if(channelId == streamings[i]["channelId"]){
            videoId = streamings[i]["videoId"];
        }
    }
    let domain = document.domain;
    let chat_url = "https://www.youtube.com/live_chat?v="+videoId+"&embed_domain="+domain;
    element_chatform.setAttribute("src", chat_url);
    element_youtube.setAttribute("src", "https://www.youtube.com/embed/live_stream?channel="+channelId+"&enablejsapi=1");
}

function closeStatusWindow(){
    yt_interval = setInterval(randomSetYouTube, speed); // restart youtube interval
    console.log("close status window.");
    element_mask.setAttribute("style", "display: none;");
    element_statusWindow.setAttribute("style", "display: none;");
}