// 幕の開閉
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
var element = document.getElementById("youtube");
var element_streamingId = document.getElementById("streamingId");
var element_streamings = document.getElementById("streamings");
var element_channelId = document.getElementById("channelId");
var element_userName = document.getElementById("userName");
var element_videoTitle = document.getElementById("videoTitle");
var element_twitterId = document.getElementById("twitterId");
var element_streamingNumber = document.getElementById("streamingNumber");

// ランダムに再生する
function randomSetYouTube(){

    var streamData;
    function StreamData(jsonData){
        streamData = jsonData;
    }
    function changeStream(jsonData){
        console.log("changeStream");

        curtainOC(); // 幕を掛ける


        if (i < jsonData.length-1){ i += 1; }
        else{ i = 0; }

        console.log("stream: "+i);
        // 動画セット
        function sleep1(){
            element.setAttribute("src", "https://www.youtube.com/embed/live_stream?channel="+jsonData[i]["channelId"]+"&autoplay=1");
            element_streamingId.innerHTML = i;
            element_streamings.innerHTML  = jsonData.length;
            element_channelId.innerHTML   = jsonData[i]["channelId"];
            element_videoTitle.innerHTML  = jsonData[i]["videoTitle"];
            element_streamingNumber.innerHTML = jsonData[i]["streamingNumber"];
            element_userName.innerHTML    = "undefined";
            element_twitterId.innerHTML   = "undefined";
            element_userName.innerHTML    = streamData[ jsonData[i]["channelId"] ]["userName"];
            element_twitterId.innerHTML   = streamData[ jsonData[i]["channelId"] ]["twitterId"];
        }
        setTimeout(sleep1, 1000); // 切り替え1秒前に幕を掛ける
        
        function sleep2(){
            curtainOC(); // 幕を開ける
        }
        setTimeout(sleep2, 4500); // 幕を掛ける時間3.5秒
    }

    $.post('getData.php?mode=getStreaming', {}, function(data){ // jQuery Post
        jsonData = JSON.parse(data);
        changeStream(jsonData);
    });
    $.post('getData.php?mode=getStreamData', {}, function(data){ // jQuery Post
        jsonData = JSON.parse(data);
        StreamData(jsonData);
    });
    
}

// 1分毎に配信を切り替えながらストリーミングする
function streaming(){
    randomSetYouTube();
}
stop = setInterval(streaming, 60000);