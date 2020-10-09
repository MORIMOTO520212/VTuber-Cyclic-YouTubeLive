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
var streamingChannel = "";
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
var element_livePoint = document.getElementById("livePoint");
var element_play = document.getElementById("play");
var element_speed = document.getElementById("speed");
var ctx = document.getElementById("myChart");

var streamings;

function intervalStreamingData(){

    function StreamingData(jsonData){

        streamings = jsonData;

        // ステータス画面の総配信者のTwitterアイコンを表示する
        var imgSource = "";
        for(var j = 0; j < streamings.length; j++){
            
            if(streamingChannel != streamings[j]["channelId"]){
                imgSource +=  "<a href=\"https://www.youtube.com/channel/"+streamings[j]["channelId"]+"\" target=\"_blank\"><img class=\"icon\" src=\"" + streamings[j]["photo"] + "\"></a>";
            
            }else{ // ハイライト
                imgSource +=  "<a href=\"https://www.youtube.com/channel/"+streamings[j]["channelId"]+"\" target=\"_blank\"><img class=\"icon hilight\" src=\"" + streamings[j]["photo"] + "\"></a>";
            }
        }
        element_streamings.innerHTML = imgSource;        
    }

    // streamingデータ取得
    $.post('getData.php?mode=getStreaming', {}, function(data){
        console.log("getStreaming");
        jsonData = JSON.parse(data);
        StreamingData(jsonData);
    });
}
intervalStreamingData();
setInterval(intervalStreamingData, 5000);

// アクティブ 棒グラフ
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

// ランダムに再生する
function randomSetYouTube(){
    console.log("randomSetYouTube");

    if (i < streamings.length-1){ i += 1; }
    else{ i = 0; }

    curtainOC(); // 幕を掛ける

    console.log("stream: "+i);
    // 動画セット
    function sleep1(){
        element_youtube.setAttribute("src", "https://www.youtube.com/embed/live_stream?channel="+streamings[i]["channelId"]+"&autoplay=1");
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
    }
    setTimeout(sleep1, 1000); // 切り替え1秒前に幕を掛ける
    
    function sleep2(){
        curtainOC(); // 幕を開ける
    }
    setTimeout(sleep2, 4500); // 幕を掛ける時間3.5秒

}

// 1分毎に配信を切り替えながらストリーミングする
var interval;
function streaming(){
    element_play.setAttribute("class", "play close");
    randomSetYouTube();
    interval = setInterval(randomSetYouTube, 60000); // 60.000秒
}
function changeSpeed(){
    console.log("changeSpeed "+element_speed.value*60000);
    clearInterval(interval);
    interval = setInterval(randomSetYouTube, element_speed.value*60000);
}


function getStreamingSource(){
    var element_getStreaming = document.getElementById("getStreaming");
    element_getStreaming.innerHTML = streamings;
}
function getStreamDataSource(){
    var element_getStreamData = document.getElementById("getStreamData");
    element_getStreamData.innerHTML = StreamData;
}