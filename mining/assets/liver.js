var element_liverlist = document.getElementById("list");
var filtering_game = ""; // filtering game product name

function getObjId(){
    return window.btoa(Math.random()*10000000000);
}
function liverViewer(){
    let source = "";
    let _streamings = [];
    let separate_index;
    for(var i=0;  i < streamings.length; i++){
        let productName = streamings[i]["play"]["product"];
        if(productName == filtering_game){
            _streamings.push(streamings[i]);
        }
    }
    separate_index = _streamings.length;
    for(var i=0;  i < streamings.length; i++){
        let productName = streamings[i]["play"]["product"];
        if(productName != filtering_game){
            _streamings.push(streamings[i]);
        }
    }
    streamings = _streamings;
    for(var i=0;  i < streamings.length; i++){
        if(i == separate_index && 0 != separate_index){
            source += "<hr>"; // separate borderline
        }else{
            /* streamings[i]["background"] // user background           */
            let channelId  = streamings[i]["channelId"]       // channelId
            let userName   = streamings[i]["userName"]        // user name
            let streamNum  = streamings[i]["streamingNumber"] // connected users number
            let videoTitle = streamings[i]["videoTitle"]      // video title
            let photo      = streamings[i]["photo"]           // user photo
            let thumbnail  = streamings[i]["thumbnailUrl"]    // video thumbnail
            source += "<li id=\""+getObjId()+"\" class=\"item\"><img class=\"background\" src=\""+thumbnail+"\"><a href=\"javascript:status(\'"+channelId+"\');\"></a><div class=\"user\"><div class=\"icon\"><img src=\""+photo+"\"></div><div class=\"name\"><p>"+userName+"</p></div></div><div class=\"watching\"><p>"+streamNum+"</p></div><div class=\"videoTitle\"><p>"+videoTitle+"</p></div></li>";
        }
    }
    element_liverlist.innerHTML = source;
}