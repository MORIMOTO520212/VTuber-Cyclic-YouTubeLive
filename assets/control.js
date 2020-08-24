// 幕の開閉
function curtainOC(){
    element = document.getElementById("curtain");
    if(element.className == "curtain open"){
        element.className = "curtain close";
        console.log("curtain close");
    }else{
        element.className = "curtain open";
        console.log("curtain open");
    }
    return;
}

var i = 0;
// ランダムに再生する
function randomSetYouTube(){
    
    var element = document.getElementById("youtube");

    function changeStream(jsonData){
        console.log("changeStream");

        curtainOC(); // 幕を掛ける


        if (i < jsonData.length){ i += 1; }
        else{ i = 0; }

        console.log("stream: "+i);
        // 動画セット
        function sleep1(){
            element.setAttribute("src", "https://www.youtube.com/embed/live_stream?channel="+jsonData[i]+"&autoplay=1");
        }
        setTimeout(sleep1, 1000); // 切り替え1秒前に幕を掛ける
        
        function sleep2(){
            curtainOC(); // 幕を開ける
        }
        setTimeout(sleep2, 4500); // 幕を掛ける時間3.5秒
    }

    $.post('getData.php?mode=getStreaming', {}, function(data){ // jQuery Post
        jsonData = JSON.parse(data);
        changeStream(jsonData);
    });
    
}

// 1分毎に配信を切り替えながらストリーミングする
function streaming(){
    randomSetYouTube();
}
stop = setInterval(streaming, 60000);