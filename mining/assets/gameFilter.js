var element_games = document.getElementById("games");
var e_game_filter_top = document.getElementById("game_filter_top");

function gameFilter() { // update game list.
    let games = [];
    let source = "";
    for(var i=0; i<streamings.length; i++){
        let play = streamings[i]["play"];
        let productName = streamings[i]["play"]["product"];
        if(!games.includes(productName) && play){
            source += `<li><a href="#" onclick="javascript:gameFiltering(\'${productName}\');return false;">${productName}</a></li>`;
            games.push(productName);
        }
    }
    source += `<li><a href="#" onclick="javascript:noneFilter();return false;">フィルター解除</a></li>`;
    element_games.innerHTML = source;
    
}
// streamings[i][play] -> [product], [url], [photo]

function gameFiltering(productName) {
    console.log("filtering: "+productName);
    filtering_game = productName;
    e_game_filter_top.innerText = filtering_game;
    liverViewer(filtering_game, false); // update
}

function noneFilter() {
    filtering_game = "";
    e_game_filter_top.innerText = "ゲーム選択";
    liverViewer(filtering_game, false); // update
}