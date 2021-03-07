var element_liverlist = document.getElementById("list");

function getObjId(){
    return window.btoa(Math.random()*10000000000);
}

function liverViewer(){
    let source = "";
    for(let i=0;  i < streamings.length; i++){
        /* streamings[i]["background"] // user background           */
        let channelId  = streamings[i]["channelId"]       // channelId
        let userName   = streamings[i]["userName"]        // user name
        let streamNum  = streamings[i]["streamingNumber"] // connected users number
        let videoTitle = streamings[i]["videoTitle"]      // video title
        let photo      = streamings[i]["photo"]           // user photo
        source += "<li id=\""+getObjId()+"\" class=\"item\"><img class=\"background\" src=\"\"><a href=\"javascript:status(\'"+channelId+"\');\"></a><div class=\"user\"><div class=\"icon\"><img src=\""+photo+"\"></div><div class=\"name\"><p>"+userName+"</p></div></div><div class=\"watching\"><p>"+streamNum+"</p></div><div class=\"videoTitle\"><p>"+videoTitle+"</p></div></li>";
    }
    element_liverlist.innerHTML = source;
}