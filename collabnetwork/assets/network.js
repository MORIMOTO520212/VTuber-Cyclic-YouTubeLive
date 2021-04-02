/*
    Playing with Physics
    https://visjs.github.io/vis-network/examples/network/physics/physicsConfiguration.html
*/

var already = [];
var nodes = [];
var edges = [];

var container = document.getElementById("mynetwork");
var msg = document.getElementById("msg");
function StreamData(jsonData){
    msg.innerHTML = "<p>ネットワークを構築中...<\/p><p>※環境によって表示されるまで2～3分かかる場合がございます。<\/p>";
    streamData = jsonData;

    Object.keys(streamData).forEach(channelId => {
        if(streamData[channelId]["collab"].length){
            // ノード作成
            nodes.push({
                id:    channelId,
                label: streamData[channelId]["userName"],
                size:  streamData[channelId]["collab"].length*2+5,
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
    console.log("Nodes");
    console.log(nodes);
    console.log("Edges");
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
            size: 10
        },
        physics: {
            barnesHut: {
                centralGravity: 0.3,
                springLength: 300,
                damping: 0.15,
                avoidOverlap: 0.2
            }
        }
    };
    var network = new vis.Network(container, data, options);
    setTimeout(function(){ msg.innerHTML = ""; }, 1000*80);
}

$.post('../getData.php?mode=getStreamData', {}, function(data){
    console.log("getStreamData");
    jsonData = JSON.parse(data);
    StreamData(jsonData);
});