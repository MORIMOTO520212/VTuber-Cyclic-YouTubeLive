var already = [];
var nodes = [];
var edges = [];

function StreamData(jsonData){
    streamData = jsonData;

    Object.keys(streamData).forEach(channelId => {
        console.log(channelId);
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
    });
}

jsonData = {
    "UCFpxoltilHCmuHWeERqsUlA": {
        "userName": "iroha_Vt",
        "photo": "https://pbs.twimg.com/profile_images/1305338435930959873/uaQNdjPt_400x400.jpg",
        "collab": ["UCfiK42sBHraMBK6eNWtsy7A"]
    },
    "UCfiK42sBHraMBK6eNWtsy7A": {
        "userName": "kashikomari_ch",
        "photo": "https://pbs.twimg.com/profile_images/1308609949115641858/hFz9Kb5h_400x400.jpg",
        "collab": ["UCflNPJUJ4VQh1hGDNK7bsFg", "UCFpxoltilHCmuHWeERqsUlA"]
    },
    "UCflNPJUJ4VQh1hGDNK7bsFg": {
        "userName": "Bell_Nekonogi",
        "photo": "https://pbs.twimg.com/profile_images/1300708675003138050/tJhC057I_400x400.jpg",
        "collab": ["UCfiK42sBHraMBK6eNWtsy7A"]
    }
}
StreamData(jsonData);
console.log(nodes);
console.log(edges);
console.log(already);

/*
$.post('../getData.php?mode=getStreamData', {}, function(data){
    console.log("getStreamData");
    jsonData = JSON.parse(data);
    StreamData(jsonData);
});
*/


var container = document.getElementById("mynetwork");
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
        size: 10,
    }
};
var network = new vis.Network(container, data, options);