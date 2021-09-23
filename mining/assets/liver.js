var element_liverlist = document.getElementById("list");
var filtering_game = ""; // filtering game product name
var channel_list = {};

/* Create random id */
function getObjId() {
    return window.btoa(Math.random()*10000000000);
}

function liverViewer() {
    let source = "";
    let _streamings = [];
    let separate_index;
    channel_list = {};
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
            let videoId = streamings[i]["videoId"];
            let listId = getObjId();
            channel_list[listId] = videoId;
            source += '\
            <li id="'+listId+'" class="item" onmouseover="smart_preview(\''+listId+'\','+true+')" onmouseout="smart_preview(\''+listId+'\','+false+')">\
                <iframe id="smart_yt" class="smart-yt" src="" style="" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>\
                <img class="background" src="'+thumbnail+'">\
                <a href="javascript:status(\''+channelId+'\');"></a>\
                <div class="user">\
                    <div class="icon"><img src="'+photo+'"></div>\
                    <div class="name"><p>'+userName+'</p></div>\
                </div>\
                <div class="watching"><p>'+streamNum+'</p></div>\
                <div class="videoTitle"><p>'+videoTitle+'</p></div>\
            </li>';
        }
    }
    element_liverlist.innerHTML = source;

    /*
    for(let list_id in channel_list){
        document.getElementById(list_id).addEventListener("mouseenter", function(event){
            setTimeout(function(){smart_preview(list_id, false)}, 500);
        });
        document.getElementById(list_id).addEventListener("mouseover", function(event){
            setTimeout(function(){smart_preview(list_id, true)}, 500);
        });
    }*/
}

function smart_preview(list_id, status) {
    if(status){
        document.getElementById(list_id).children[0].setAttribute("src", "https://www.youtube.com/embed/"+channel_list[list_id]+"?autoplay=1&mute=1&controls=0&modestbranding=0&showinfo=0");
    }else{
        document.getElementById(list_id).children[0].setAttribute("src", "");
    }
}

