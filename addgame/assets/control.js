var games;

// 検索名欄ID
var searchNameIds = array();
// 製品名欄ID
var productNameIds = array();
// 製品リンクID
var officialSiteLinkIds = array();
// 製品画像ID
var ProductPhotoIds = array();


function getGames(jsonData){
    games = jsonData;
}
$.post('getData.php?mode=getGames_local', {}, function(data){
    console.log("getGames_local");
    jsonData = JSON.parse(data);
    getGames(jsonData);
});