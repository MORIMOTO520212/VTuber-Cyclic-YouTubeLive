var already = [];
var nodes = [];
var edges = [];

var container = document.getElementById("mynetwork");

function StreamData(jsonData){
    streamData = jsonData;

    Object.keys(streamData).forEach(channelId => {
        if(streamData[channelId]["collab"].length){
            // ノード作成
            nodes.push({
                id:    channelId,
                label: streamData[channelId]["userName"],
                size:  streamData[channelId]["collab"].length*2+10,
                image: streamData[channelId]["photo"]
            });
            // エッジ作成
            streamData[channelId]["collab"].forEach(collab_ch => {
                var check = true;
                already.forEach(already_ch => {
                    if(collab_ch == already_ch){ check = false; }
                });
                if(check){
                    edges.push({
                        from: channelId,
                        to: collab_ch
                    });
                }
            });
            // エッジ済みID
            already.push(channelId);
        }
    });

    console.log(nodes);
    console.log(edges);

    var data = {
        nodes: nodes,
        edges: edges
    };
    var options = {
        autoResize: true,
        height: '100%',
        width: '100%',
        nodes: {
            shape: "circularImage",
            font: {
                color: "#eee"
            },
            brokenImage: "assets/favicon.png",
            size: 10,
        }
    };
    var network = new vis.Network(container, data, options);
}

$.post('../getData.php?mode=getStreamData', {}, function(data){
    console.log("getStreamData");
    jsonData = JSON.parse(data);
    StreamData(jsonData);
});