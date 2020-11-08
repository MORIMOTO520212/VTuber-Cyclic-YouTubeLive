var streamData = new Array();
var dateList = new Array();

function parseDate(date, lastLiveDate){
    var ymdhs = lastLiveDate.split(/[\/: ]/);
    var ch_dt = new Date(Number(ymdhs[0]), Number(ymdhs[1])-1, Number(ymdhs[2]), Number(ymdhs[3]), Number(ymdhs[4]), Number(ymdhs[5]));
    var diff = (date.getTime() - ch_dt.getTime()) / (1000*60*60*24); // diffは小数点を切り捨て
    return parseInt(diff);
}

function sort(streamData, dateList){
    dateList.sort(function(a, b) {
        if (a[1] > b[1]) { return 1; }
        else{ return -1; }
    });
    var date = new Date();
    dateList.forEach(channelId0 => {
        channel = streamData[channelId0[0]];
        var diff_day = parseDate(date, channel["lastLiveDate"]);
        document.write(diff_day+"日前に配信  "+channel["userName"]+"<br>");
    });
}

function reverse(streamData, dateList){
    dateList.sort(function(a, b) {
        if (a[1] < b[1]) { return 1; }
        else{ return -1; }
    });
    var date = new Date();
    dateList.forEach(channelId0 => {
        channel = streamData[channelId0[0]];
        var diff_day = parseDate(date, channel["lastLiveDate"]);
        document.write(diff_day+"日前に配信  "+channel["userName"]+"<br>");
    });
}

function StreamingData(streamData){
    Object.keys(streamData).forEach(channelId => {
        dateList.push( Array(channelId, Number(streamData[channelId]["lastLiveDate"].replace(/[\/: ]/g, ""))));
    });
    sort(streamData, dateList);
}
$.post('../getData.php?mode=getStreamData', {}, function(data){
    console.log("getStreamData");
    jsonData = JSON.parse(data);
    StreamingData(jsonData);
});

/*
        console.log("ChannelId: "+channelId);
        console.log("userName: "+streamData[channelId]["userName"]);
        console.log("TwitterId:"+streamData[channelId]["twitterId"]);
        console.log("photo: "+streamData[channelId]["photo"]);
        console.log("livePoint: "+streamData[channelId]["livePoint"]);
        console.log("lastLiveDate: "+streamData[channelId]["lastLiveDate"]);
*/