/* * * * * * * * * * * * * * * * * * *

    VTuber Cyclic Live Streaming 
    update: 2020/10/13
    GitHub:
    Twitter: @Medaka_bridle

* * * * * * * * * * * * * * * * * * */



var streamingChannel    = "";
var element_youtube     = document.getElementById("youtube");
var element_streamings  = document.getElementById("streamings");
var element_channelId   = document.getElementById("channelId");
var element_userName    = document.getElementById("userName");
var element_twitterId   = document.getElementById("twitterId");
var element_videoTitle  = document.getElementById("videoTitle");
var element_playgame_photo  = document.getElementById("playgame_photo");
var element_playgame_link   = document.getElementById("playgame_link");
var element_streamingNumber = document.getElementById("streamingNumber");
var element_livePoint       = document.getElementById("livePoint");
var element_counter         = document.getElementById("counter");
var element_embed_verify    = document.getElementById("embedVerify");
var visual_main             = document.getElementById("visual_main");



/* Streaming Update 5.0s */
var streamings;
var usrCounter;
function intervalStreamingData(){
    function StreamingData(jsonData){
        streamings = jsonData;

        var imgSource = "";
        for(var j = 0; j < streamings.length; j++){
            imgSource +=  "<div id=\"" + streamings[j]["channelId"] + "\" class=\"box\"><a href=\"javascript:setYouTube(\'" + streamings[j]["channelId"] + "\');\"><div class=\"img\"><img src=\"" + streamings[j]["photo"] + "\"></div><div class=\"name\"><p>" + streamings[j]["userName"] + "</p></div><div class=\"title\"><p>" + streamings[j]["videoTitle"] + "</p></div></a><div class=\"ck\"><div><a href=\"https://twitter.com/" + streamings[j]["twitterId"] + "\" target=\"_blank\" rel=\"noopener\"><img src=\"assets/Twitter_Logo_WhiteOnBlue.png\"></a></div><div><a href=\"https://www.youtube.com/channel/" + streamings[j]["channelId"] + "\" target=\"_blank\" rel=\"noopener\"><img src=\"assets/yt_icon_rgb.png\"></a></div><div class=\"badge\"><img src=\"assets/badge.png\"></div></div></div>";
        }
        element_streamings.innerHTML = imgSource;
        element_counter.innerHTML = "<p>" + streamings.length + "人</p>"; // Number Counter
    }
    $.post('../getData.php?mode=getStreaming', {}, function(data){ // Get Data
        console.log("getStreaming");
        jsonData = JSON.parse(data);
        StreamingData(jsonData);
    });
}
intervalStreamingData();
setInterval(intervalStreamingData, 5000);


/* Streaming */
var videoId;
function setYouTube(channelId){
    console.log("setYouTube");
    element_youtube.setAttribute("src", "https://www.youtube.com/embed/live_stream?channel="+channelId+"&enablejsapi=1");
    var ch_metadata = streamings.filter(elem => {
        return channelId == elem.channelId;
    });
    element_channelId.innerText       = channelId;
    element_userName.innerText        = ch_metadata[0].userName;
    element_twitterId.innerText       = ch_metadata[0].twitterId;
    element_streamingNumber.innerText = ch_metadata[0].streamingNumber;
    element_videoTitle.innerText      = ch_metadata[0].videoTitle;
    element_livePoint.innerText       = ch_metadata[0].livePoint;
    
    if(ch_metadata[0].play){
        console.log(ch_metadata[0].play);
        element_playgame_photo.setAttribute("src", ch_metadata[0].play.photo);
        element_playgame_link.setAttribute("href", ch_metadata[0].play.url);
    }
    
}



/* YouTube iframe api */
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

/* embed verify */
function embed_verify() {
    channelId = element_embed_verify.value;
    channelId = channelId.replace("https://www.youtube.com/channel/", "");
    setYouTube(channelId);
}



/* stream data editor */
var streamData;
var streamElementSource;
function StreamData(jsonData){
    stremData = jsonData;
    streamElementSource = "<p>{</p>";
    Object.keys(stremData).forEach(channelId => {
        let userName = stremData[channelId]["userName"];
        let twitterId = stremData[channelId]["twitterId"];
        let photo = stremData[channelId]["photo"];
        streamElementSource += "<div class=\"channelId\"><input type=\"text\" id=\"\" value=\""+ channelId +"\"><p>: {</p></div><div class=\"elem2 userName\"><p>\"userName\": </p><input type=\"text\" id=\"\" value=\""+ userName +"\"></div><div class=\"elem2 twitterId\"><p>\"twitterId\": </p><input type=\"text\" id=\"\" value=\""+ twitterId +"\"></div><div class=\"elem2 photo\"><p>\"photo\": </p><input type=\"text\" id=\"\" value=\""+ photo +"\"></div><p class=\"ct\">},</p>";
    });
    streamElementSource += "<p>}</p>";
    visual_main.innerHTML = streamElementSource;
}
$.post('../getData.php?mode=getStreamData', {}, function(data){
    console.log("getStreamData");
    jsonData = JSON.parse(data);
    StreamData(jsonData);
});

/* get message log */
function messageLog(data){
    
}
$.ajax({
    type: 'POST',
    url: '../getData.php?mode=message_log',
    dataType: 'html',
    success: function(data){
        messageLog(data);
    }
});