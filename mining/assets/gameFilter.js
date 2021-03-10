var element_games = document.getElementById("games");

function gameFilter(){
    let games = [];
    let source = "";
    for(var i=0; i<streamings.length; i++){
        let play = streamings[i]["play"];
        let productName = streamings[i]["play"]["product"];
        if(!games.includes(productName) && play){
            source += "<li><a href=\"#\" onclick=\"return false;\">"+productName+"</a></li>";
            games.push(productName);
        }
    }
    source += "<li><a href=\"#\" onclick=\"return false;\">フィルター解除</a></li>";
    element_games.innerHTML = source;
}
// streamings[i][play] -> [product], [url], [photo]