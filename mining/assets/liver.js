var element_liverlist = document.getElementById("list");
var channel_list = {};

/* Create random id */
function getObjId() {
    return window.btoa(Math.random()*10000000000);
}

/* 同時接続者数の表示形式を変換 */
function parseWatchNumber(str) {
    if(str.match("万人")){
        return Number(str.replace("万人", ""))*10000;
    }else{
        return Number(str.replace("人", ""));
    }
}

function liverViewer(filtering_game, sortAudience) {
    // filtering_game - フィルタリングするゲーム名、なしは空白
    // sortAudience - true/false 同時接続者数でソートするか

    /* streamingsはグローバル */
    let source = "";
    let _streamings = [];
    let separate_index;
    channel_list = {};

    /* 同時接続者数でソートする */
    if(sortAudience){
        for(var i=0;  i < streamings.length; i++){
            streamings[i]["audienceOrder"] = parseWatchNumber(streamings[i]["streamingNumber"]); // 同時接続者数
        }
        streamings.sort((a,b) => b.audienceOrder - a.audienceOrder);
    }

    /* 初めにゲームフィルターとマッチするゲームの動画を配列に格納 */
    for(var i=0;  i < streamings.length; i++){
        let productName = streamings[i]["play"]["product"];
        if(productName == filtering_game){
            _streamings.push(streamings[i]);
        }
    }
    separate_index = _streamings.length; // 区切りのindexを取得

    /* ゲームフィルターとマッチしなかった動画を配列に格納 */
    for(var i=0;  i < streamings.length; i++){
        let productName = streamings[i]["play"]["product"];
        if(productName != filtering_game){
            _streamings.push(streamings[i]);
        }
    }
    streamings = _streamings; // 配列 書き換え

    /* 年末年始　フィルター */
    function HappyNewYear() {
        let happyNewYearWords = ["年末", "年越し", "大掃除", "大晦日", "年明け", "正月"];
        for(var i=0; i < streamings.length; i++){
            let videoTitle = streamings[i]["videoTitle"];
            /* 動画タイトルから特定ワードの検索 */
            for(var j=0; j < happyNewYearWords.length; j++){
                if(videoTitle.match(happyNewYearWords[j])){
                    /* streamings[i]["background"] // ユーザーバックグラウンド */
                    let channelId  = streamings[i]["channelId"]       // Channel ID
                    let userName   = streamings[i]["userName"]        // ユーザー名
                    let streamNum  = streamings[i]["streamingNumber"] // 同時接続者数
                    let videoTitle = streamings[i]["videoTitle"]      // 動画タイトル
                    let photo      = streamings[i]["photo"]           // ユーザーアイコン
                    let thumbnail  = streamings[i]["thumbnailUrl"]    // 動画サムネイル
                    let videoId = streamings[i]["videoId"];
                    let listId = getObjId();
                    channel_list[listId] = videoId;
                    source += `
                    <li id="${listId}" class="item" onmouseover="smart_preview('${listId}', true)" onmouseout="smart_preview('${listId}', false)">
                        <iframe id="smart_yt" class="smart-yt" src="" style="" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
                        <img class="background" src="${thumbnail}">
                        <a href="javascript:status('${channelId}');"></a>
                        <div class="user">
                            <div class="icon"><img src="${photo}"></div>
                            <div class="name"><p>${userName}</p></div>
                        </div>\
                        <div class="watching"><p>${streamNum}</p></div>
                        <div class="videoTitle"><p>${videoTitle}</p></div>
                    </li>`;
                    break;
                }
            };
        }
        source += "<hr>";
    }
    HappyNewYear();

    for(var i=0;  i < streamings.length; i++){
        /* ゲームフィルターが有効な場合、線を引いて分割 */
        if(i == separate_index && 0 != separate_index){
            source += "<hr>";
        }else{
            /* streamings[i]["background"] // ユーザーバックグラウンド */
            let channelId  = streamings[i]["channelId"]       // Channel ID
            let userName   = streamings[i]["userName"]        // ユーザー名
            let streamNum  = streamings[i]["streamingNumber"] // 同時接続者数
            let videoTitle = streamings[i]["videoTitle"]      // 動画タイトル
            let photo      = streamings[i]["photo"]           // ユーザーアイコン
            let thumbnail  = streamings[i]["thumbnailUrl"]    // 動画サムネイル
            let videoId = streamings[i]["videoId"];
            let listId = getObjId();
            channel_list[listId] = videoId;
            source += `
            <li id="${listId}" class="item" onmouseover="smart_preview('${listId}', true)" onmouseout="smart_preview('${listId}', false)">
                <iframe id="smart_yt" class="smart-yt" src="" style="" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
                <img class="background" src="${thumbnail}">
                <a href="javascript:status('${channelId}');"></a>
                <div class="user">
                    <div class="icon"><img src="${photo}"></div>
                    <div class="name"><p>${userName}</p></div>
                </div>\
                <div class="watching"><p>${streamNum}</p></div>
                <div class="videoTitle"><p>${videoTitle}</p></div>
            </li>`;
        }
    }
    element_liverlist.innerHTML = source;
}