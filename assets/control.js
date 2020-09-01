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
var element_youtube = document.getElementById("youtube");
var element_streamingId = document.getElementById("streamingId");
var element_streamings = document.getElementById("streamings");
var element_channelId = document.getElementById("channelId");
var element_userName = document.getElementById("userName");
var element_videoTitle = document.getElementById("videoTitle");
var element_twitterId = document.getElementById("twitterId");
var element_streamingNumber = document.getElementById("streamingNumber");
var element_main_userName = document.getElementById("main_userName");
var element_main_videoTitle = document.getElementById("main_videoTitle");
var element_photo = document.getElementById("photo");

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
            element_youtube.setAttribute("src", "https://www.youtube.com/embed/live_stream?channel="+jsonData[i]["channelId"]+"&autoplay=1");
            element_streamingId.innerHTML      = i;                                // ステータス画面のストリーミング番号
            element_streamings.innerHTML       = jsonData.length;                  // ステータス画面の総配信者数
            element_channelId.innerHTML        = jsonData[i]["channelId"];         // ステータス画面のチャンネルID
            element_videoTitle.innerHTML       = jsonData[i]["videoTitle"];        // ステータス画面の動画タイトル
            element_main_videoTitle.innerHTML  = jsonData[i]["videoTitle"];        // メイン画面の動画タイトル
            element_streamingNumber.innerHTML  = jsonData[i]["streamingNumber"];   // ステータス画面の同時接続者数
            element_userName.innerHTML         = "undefined";
            element_twitterId.innerHTML        = "undefined"; // 見つからなかった場合はundefinedを表示する
            element_main_userName.innerHTML    = "undefined"; 
            element_userName.innerHTML         = streamData[ jsonData[i]["channelId"] ]["userName"];  // ステータス画面のユーザー名
            element_twitterId.innerHTML        = streamData[ jsonData[i]["channelId"] ]["twitterId"]; // ステータス画面のTwitterID
            element_main_userName.innerHTML    = streamData[ jsonData[i]["channelId"] ]["userName"];  // メイン画面のユーザー名
            element_photo.setAttribute("src", streamData[ jsonData[i]["channelId"] ]["photo"]);       // メイン画面のTwitterアイコン

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