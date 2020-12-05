var games = [];

// 検索名欄ID
var searchNameIds = [];
// 製品名欄ID
var productNameIds = [];
// 製品リンクID
var officialSiteLinkIds = [];
// 製品画像ID
var ProductPhotoIds = [];

window.onload = function() {
    xhr = new XMLHttpRequest();
    // サーバからのデータ受信を行った際の動作
    xhr.onload = function (e) {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var answer = document.getElementById('answer');
                answer.value = xhr.responseText;
            }
        }
    };
};
function post(data) {
    xhr.open('POST', 'assets/write.php', true);
    xhr.setRequestHeader("Content-Type", "application/json");
    // フォームに入力した値をリクエストとして設定
    xhr.onload = () => {
        console.log(xhr.status);
        console.log("success!");
    };
    xhr.onerror = () => {
        console.log(xhr.status);
        console.log("error!");
    };
    xhr.send(JSON.stringify(data));
}


viewElement = document.getElementById("main");

function getObjId(){
    return window.btoa(Math.random()*10000000000);
}

/* 
    SNid  - Search Name ID
    PNid  - Product Name ID
    OSLid - Official Site Link ID
    PPid  - Product Photo ID
    SNV   - Search Name Value
    PNV   - Product Name Value
    OSLV  - Official Site Link Value
    PPV   - Product Photo Value
*/
function createSrc(index, SNid, PNid, OSLid, PPid, SNV, PNV, OSLV, PPV){
    if(!(SNV)){ SNV = "" };
    if(!(PNV)){ PNV = "" };
    if(!(OSLV)){ OSLV = "" };
    if(!(PPV)){ PPV = "" };
    source = "<p>Index "+index+"</p><a href=\"javascript:del("+index+")\">削除</a><div class=\"input-main searchName\"><input type=\"text\" id=\""+SNid+"\" placeholder=\"検索名\" value=\""+SNV+"\"></div>";
    source += "<div class=\"input-main productName\"><input type=\"text\" id=\""+PNid+"\" placeholder=\"製品名\"value=\""+PNV+"\"></div>";
    source += "<div class=\"input-main officialSiteLink\"><input type=\"text\" id=\""+OSLid+"\" placeholder=\"公式サイトリンク\" value=\""+OSLV+"\"></div>";
    source += "<div class=\"input-main productPhoto\"><input type=\"text\" id=\""+PPid+"\" placeholder=\"画像リンク\" value=\""+PPV+"\"></div>";
    return source;
}

function WRITE(HTML){
    viewElement.innerHTML = HTML;
}

function viewDB(){
    // inner HTML write
    var HTML = "";
    for(var i = 0; i < games.length; i++){
        var SNid  = searchNameIds[i];
        var PNid  = productNameIds[i];
        var OSLid = officialSiteLinkIds[i];
        var PPid  = ProductPhotoIds[i];
        var SNV   = games[i]["word"];
        var PNV   = games[i]["product"];
        var OSLV  = games[i]["url"];
        var PPV   = games[i]["photo"];
        HTML += createSrc(i, SNid, PNid, OSLid, PPid, SNV, PNV, OSLV, PPV);
    }
    return HTML;
}

function submit(){
    for(var i = 0; i < games.length; i++){
        var SNid  = searchNameIds[i];
        var PNid  = productNameIds[i];
        var OSLid = officialSiteLinkIds[i];
        var PPid  = ProductPhotoIds[i];
        var SearchName  = document.getElementById(SNid).value;
        var ProductName = document.getElementById(PNid).value;
        var OfficialSiteLink = document.getElementById(OSLid).value;
        var ProductPhoto = document.getElementById(PPid).value;
        games[i]["word"]    = SearchName;
        games[i]["product"] = ProductName;
        games[i]["url"]     = OfficialSiteLink;
        games[i]["photo"]   = ProductPhoto;
    }
}

function add(){
    submit();
    searchNameIds.push(getObjId());
    productNameIds.push(getObjId());
    officialSiteLinkIds.push(getObjId());
    ProductPhotoIds.push(getObjId());
    games.push({"word": false, "product": false, "url": false, "photo": false});
    /* write */
    var HTML = viewDB();
    WRITE(HTML);
}

function del(index){
    games.splice(index,1);
    searchNameIds.splice(index,1);
    productNameIds.splice(index,1);
    officialSiteLinkIds.splice(index,1);
    ProductPhotoIds.splice(index,1);
    /* write */
    var HTML = viewDB();
    WRITE(HTML);
}

function send(){
    submit();
    post(games);
}

function getGames(jsonData){
    games = jsonData;
    games.forEach(element => {
        searchNameIds.push(getObjId());
        productNameIds.push(getObjId());
        officialSiteLinkIds.push(getObjId());
        ProductPhotoIds.push(getObjId());
    });
    var HTML = viewDB();
    WRITE(HTML);
}
$.post('../getData.php?mode=getGames_local', {}, function(data){
    console.log("getGames_local");
    jsonData = JSON.parse(data);
    getGames(jsonData);
});