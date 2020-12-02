var streamData = new Array();
var dateList = new Array();
var body = document.getElementById("main");
var source = "";

function parseDate(date, lastLiveDate){
    var ymdhs = lastLiveDate.split(/[\/: ]/);
    var ch_dt = new Date(Number(ymdhs[0]), Number(ymdhs[1])-1, Number(ymdhs[2]), Number(ymdhs[3]), Number(ymdhs[4]), Number(ymdhs[5]));
    var diff = (date.getTime() - ch_dt.getTime()) / (1000*60*60*24); // diffは小数点を切り捨て
    return parseInt(diff);
}

function DocumentWrite(userName, photo, channelId, twitterId, gameProductPhoto, diff_day){
    source += " \
    <div class=\"userlist\"><div class=\"user\"> \
    <div class=\"icon\"><img src=\""+photo+"\"></div> \
    <div class=\"sep\"> \
    <div class=\"name\"><p>"+userName+"</p></div> \
    <div class=\"youtube\"><a href=\"https://www.youtube.com/channel/"+channelId+"\" target=\"_blank\"><img src=\"assets/yt_icon_rgb.png\"></a></div> \
    <div class=\"twitter\"><a href=\"https://twitter.com/"+twitterId+"\" target=\"_blank\"><img src=\"assets/Twitter_Logo_WhiteOnBlue.png\"></a></div> \
    </div>";
    
    if(gameProductPhoto){
        source += "<div class=\"genre\"><p>最近プレイしたゲーム</p><a href=\"\"><img src=\""+gameProductPhoto+"\"></a></div>";
    }
    
    source += "<div class=\"collaboration\"></div> \
    <div class=\"mainStatus\"> \
    <div class=\"averageLiveTime\"><p>平均ライブ時間："+undefined+"</p></div> \
    <div class=\"lastlive\"><p>最終配信日："+diff_day+"日前</p></div> \
    </div> \
    <div class=\"active\"></div> \
    </div> \
    </div>";
}

function sort_Date(){
    source = "";
    dateList.sort(function(a, b) {
        if (a[1] > b[1]) { return 1; }
        else{ return -1; }
    });
    var date = new Date();
    dateList.forEach(channelId0 => {
        channel = streamData[channelId0[0]];
        var diff_day = parseDate(date, channel["lastLiveDate"]);
        var gameProductPhoto = false;
        if(channel["games"].length){
            var lastGameIndex = channel["games"].length-1;
            gameProductPhoto = channel["games"][lastGameIndex]["photo"];
        }
        DocumentWrite(channel["userName"], channel["photo"], channelId0[0], channel["twitterId"], gameProductPhoto, diff_day);
    });
    body.innerHTML = source;
}

function reverse_Date(){
    source = "";
    dateList.sort(function(a, b) {
        if (a[1] < b[1]) { return 1; }
        else{ return -1; }
    });
    var date = new Date();
    dateList.forEach(channelId0 => {
        channel = streamData[channelId0[0]];
        var diff_day = parseDate(date, channel["lastLiveDate"]);
        var gameProductPhoto = false;
        if(channel["games"].length){
            var lastGameIndex = channel["games"].length-1;
            gameProductPhoto = channel["games"][lastGameIndex]["photo"];
        }
        DocumentWrite(channel["userName"], channel["photo"], channelId0[0], channel["twitterId"], gameProductPhoto, diff_day);
    });
    body.innerHTML = source;
}

function StreamingData(jsonData){
    streamData = jsonData;
    Object.keys(streamData).forEach(channelId => {
        dateList.push( Array(channelId, Number(streamData[channelId]["lastLiveDate"].replace(/[\/: ]/g, ""))));
    });
    sort_Date();
}
$.post('../getData.php?mode=getStreamData', {}, function(data){
    console.log("getStreamData");
    jsonData = JSON.parse(data);
    StreamingData(jsonData);
});

