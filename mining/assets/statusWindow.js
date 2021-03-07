var element_youtube = document.getElementById("youtube");
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
    // stop youtube interval
    clearInterval(yt_interval); // stop interval
    element_yt.setAttribute("src", "../startpage.html"); // set top page

    console.log("status "+channelId);
    element_mask.setAttribute("style", "display: block;"); // set mask
    element_statusWindow.setAttribute("style", ""); // status window on display
    let videoId;
    for(let i=0;  i < streamings.length; i++){
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
    // start youtube interval
    randomSetYouTube();
    yt_interval = setInterval(randomSetYouTube, speed);

    console.log("close status window.");
    element_mask.setAttribute("style", "display: none;"); // close mask
    element_statusWindow.setAttribute("style", "display: none;"); // close window
    element_chatform.setAttribute("src", ""); // close chat
    element_youtube.setAttribute("src", ""); // close youtube
}