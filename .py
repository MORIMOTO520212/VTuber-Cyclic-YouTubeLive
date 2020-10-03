import json, settings

streamingChannels = [
    {
        "channelId": "UCb5JxV6vKlYVknoJB8TnyYg",
        "streamingNumber": "2260\u4eba",
        "videoTitle": "\u3010#\u30de\u30ea\u30aa35\u3011\uff11\u4f4d\u76ee\u6307\u3057\u3066\u30de\u30ea\u30aa\u30d0\u30c8\u30ed\u30ef\u3010\u9edb \u7070 / \u306b\u3058\u3055\u3093\u3058\u3011"
    },
    {
        "channelId": "UCRqBKoKuX30ruKAq05pCeRQ",
        "streamingNumber": "485\u4eba",
        "videoTitle": "\u3010\u30b9\u30d1\u30c1\u30e3\u8aad\u307f\u3011\u307f\u3066\u307f\u3066\u5317\u5c0f\u8def\u30bf\u30b0\u3082\u773a\u3081\u305f\u308a\u3010\u306b\u3058\u3055\u3093\u3058/\u5317\u5c0f\u8def\u30d2\u30b9\u30a4\u3011"
    },
    {
        "channelId": "UC_4tXjqecqox5Uc05ncxpxg",
        "streamingNumber": "4442\u4eba",
        "videoTitle": "\u3010\u539f\u795e\u3011\uff14\u4eba\u3067\u30de\u30eb\u30c1\u3059\u308b\u3093\u3060\uff5e\u2669\u304b\u306a\u304b\u306a\u821e\u5143\u30ea\u30aa\u30f3\u3010\u690e\u540d\u552f\u83ef/\u306b\u3058\u3055\u3093\u3058\u3011"
    },
    {
        "channelId": "UCQLyq7TDKHlmp2Ufd5Z2qMw",
        "streamingNumber": "16\u4eba",
        "videoTitle": "\u3010#\u539f\u795e\u3011\u3053\u306e\u30b2\u30fc\u30e0\u3084\u308b\u3053\u3068\u591a\u3059\u304e\uff5e\uff5e\uff5e\uff01\uff01\u3010#Vtuber\u3011"
    },
    {
        "channelId": "UCdpUojq0KWZCN9bxXnZwz5w",
        "streamingNumber": "4894\u4eba",
        "videoTitle": "#03\u3010\u539f\u795e\u3011\u30ac\u30c1\u30e3\u306e\u6642\u9593\u3060\u3041\u3042\u3042\u3042\u3042\u3010\u30a2\u30eb\u30b9\u30fb\u30a2\u30eb\u30de\u30eb/\u306b\u3058\u3055\u3093\u3058\u3011"
    },
    {
        "channelId": "UCMAc88lqzqGV0uxgw9JDj0w",
        "streamingNumber": "739\u4eba",
        "videoTitle": "\u3010ASMR/\u767d3dio\u3011\u4eca\u65e5\u30821\u65e5\u304a\u3064\u304b\u308c\u3055\u307e\u306a\u306e\u3058\u3083\uff01\u3010\u8033\u30de\u30c3\u30b5\u30fc\u30b8/\u8033\u3092\u585e\u3050\u97f3/\u30bf\u30c3\u30d4\u30f3\u30b0/\u8033\u306f\u3080\u3011"
    },
    {
        "channelId": "UCspv01oxUFf_MTSipURRhkA",
        "streamingNumber": "1\u4e07\u4eba",
        "videoTitle": "\u539f\u795e \uff5c #6 \u3055\u3089\u3070\u30e2\u30f3\u30c9\uff01\u3053\u3093\u306b\u3061\u306f\u7483\u6708\uff01\u203b\u9014\u4e2d\u3067\u30de\u30eb\u30c1\u4e88\u5b9a \u3010\u306b\u3058\u3055\u3093\u3058/\u53f6\u3011"
    },
    {
        "channelId": "UCfipDDn7wY-C-SoUChgxCQQ",
        "streamingNumber": "963\u4eba",
        "videoTitle": "\u3010\u30b9\u30fc\u30d1\u30fc\u30de\u30ea\u30aa 3D\u30b3\u30ec\u30af\u30b7\u30e7\u30f3\u3011\u6df1\u591c\u306e\u795e\u30b2\u30fc\u30b3\u30ec\u30af\u30b7\u30e7\u30f3\uff01\uff08\u521d\u898b\uff09\u3010\u30b9\u30fc\u30d1\u30fc\u30de\u30ea\u30aa64\u3011\u3010\u8449\u5c71\u821e\u9234/\u306b\u3058\u3055\u3093\u3058\u3011"
    },
    {
        "channelId": "UCl1oLKcAq93p-pwKfDGhiYQ",
        "streamingNumber": "720\u4eba",
        "videoTitle": "\u30b8\u30f3\u98f2\u3093\u3067\u4eba\u751f\u3092\u304b\u3093\u304c\u3048\u308b\u3002(\u304b\u3082\u3057\u308c\u306a\u3044)\u3010\u3048\u307e\u2605\u304a\u3046\u304c\u3059\u3068/\u306b\u3058\u3055\u3093\u3058\u6240\u5c5e\u3011"
    },
    {
        "channelId": "UCCVwhI5trmaSxfcze_Ovzfw",
        "streamingNumber": "4677\u4eba",
        "videoTitle": "\u3010\u30de\u30a4\u30af\u30e9\u3011\u304a\u3058\u3055\u3093\u306b\u3001\u304a\u6d12\u843d\u306a\u5e97\u3092\u6301\u305f\u305b\u3066\u3084\u308b\u306e\u3060\u203c\u3010\u5922\u6708\u30ed\u30a2\u3011"
    },
    {
        "channelId": "UCflNPJUJ4VQh1hGDNK7bsFg",
        "streamingNumber": "97\u4eba",
        "videoTitle": "\ud83d\udd14\u3010Apex\u3011\u306b\u3085\u30fc\u3044\u3084\u307b\u3093\u307b\u3063\u307b\u304c\u3068\u3069\u3044\u305f\u306e\u3067\u52dd\u3066\u308b\ud83d\udd14\u3010ViViD/ #\u732b\u8292\u30d9\u30eb\u3011"
    },
    {
        "channelId": "UCNA0XC_zxS63d4Q-JMIMyug",
        "streamingNumber": "146\u4eba",
        "videoTitle": "\u307e\u3063\u305f\u308a\u30d5\u30a9\u30fc\u30eb\u30ac\u30a4\u30ba\uff01\u300cFall Guys\uff1aUltimate Knockout\u300d"
    },
    {
        "channelId": "UCRvpMpzAXBRKJQuk-8-Sdvg",
        "streamingNumber": "315\u4eba",
        "videoTitle": "\u3010Among Us\u3011\u3051\u3093\u304d\u3055\u3093\u3068\u305f\u304f\u3055\u3093\u306e\u304a\u53cb\u9054\u3010\u65e5\u30ce\u9688\u3089\u3093 / \u3042\u306b\u307e\u30fc\u308c\u3011"
    },
    {
        "channelId": "UCV5ZZlLjk5MKGg3L0n0vbzw",
        "streamingNumber": "1.5\u4e07\u4eba",
        "videoTitle": "\u3010\u539f\u795e\u3011\u524d\u534a:\u30ac\u30c1\u30e3\uff01\u5f8c\u534a:\u304b\u306a\u304b\u306a\u30fb\u821e\u5143\u30fb\u690e\u540d\u3068\u30de\u30eb\u30c1\u3010\u306b\u3058\u3055\u3093\u3058/\u9df9\u5bae\u30ea\u30aa\u30f3\u3011"
    },
    {
        "channelId": "UCwL6XFWwPMNKX9qTyEzOmCA",
        "streamingNumber": "34\u4eba",
        "videoTitle": "\u3010#FallGuys\u3011\u30af\u30e9\u30a6\u30f3\u8010\u4e45\uff5e\u305d\u3057\u3066\u4f1d\u8aac\u3078\u2026\uff5e\u3010Vtuber/\u845b\u57ce\u4e03\u702c\u3011"
    },
    {
        "channelId": "UCllKI7VjyANuS1RXatizfLQ",
        "streamingNumber": "2758\u4eba",
        "videoTitle": "\u3010Minecraft\u3011\u30d5\u30df\u3061\u3083\u3093\u3068\u306b\u3058\u9bd6\u591c\u66f4\u304b\u3057\uff8f\uff72\uff78\uff97\u3010\u306b\u3058\u3055\u3093\u3058/\u5c71\u795e\u30ab\u30eb\u30bf\u3011"
    },
    {
        "channelId": "UC6wvdADTJ88OfIbJYIpAaDA",
        "streamingNumber": "5125\u4eba",
        "videoTitle": "\u3010\u30de\u30ea\u30aa35\u3011\u30de\u30ea\u30aa\u30e1\u30fc\u30ab\u30fc\u6700\u5f37\u306b\u3088\u308b\u65b0\u4f5c\u30d0\u30c8\u30ed\u30ef\u3010\u306b\u3058\u3055\u3093\u3058\u3011"
    },
    {
        "channelId": "UCvInZx9h3jC2JzsIzoOebWg",
        "streamingNumber": "2584\u4eba",
        "videoTitle": "\u3010SUPER MARIO BROS. 35\u3011\u30de\u30ea\u30aa\u30d0\u30c8\u30ed\u30ef\uff01\uff1f\u79c1\u306e\u30de\u30ea\u30aa\u306b\u30af\u30ea\u30dc\u30fc\u5897\u3084\u3057\u305f\u306e\u8ab0\uff01\uff01\uff01\u3010\u30db\u30ed\u30e9\u30a4\u30d6/\u4e0d\u77e5\u706b\u30d5\u30ec\u30a2\u3011"
    },
    {
        "channelId": "UC1uv2Oq6kNxgATlCiez59hw",
        "streamingNumber": "4917\u4eba",
        "videoTitle": "\u3010Minecraft\u3011\ud83d\udc21\u5e38\u95c7\u30a6\u30a9\u30fc\u30bf\u30fc\u30d1\u30fc\u30af\u4f5c\u6210\ud83d\udc21Day2\u3010\u5e38\u95c7\u30c8\u30ef/\u30db\u30ed\u30e9\u30a4\u30d6\u3011"
    },
    {
        "channelId": "UCqm3BQLlJfvkTsX_hvm0UmA",
        "streamingNumber": "8688\u4eba",
        "videoTitle": "\u3010Getting Over It with Bennett Foddy\u3011I\u2019ll do my best!!\u3010\u89d2\u5dfb\u308f\u305f\u3081/\u30db\u30ed\u30e9\u30a4\u30d6\uff14\u671f\u751f\u3011"
    },
    {
        "channelId": "UC66DRsVkzrPAp6hZV7-HBGw",
        "streamingNumber": "159\u4eba",
        "videoTitle": "\u3010\u30af\u30e9\u30c3\u30b7\u30e5\u30d0\u30f3\u30c7\u30a3\u30af\u30fc\u3011 \u3044\u3051\u308b\u3068\u601d\u3063\u305f\u3070\u3063\u3066\u3093\u3084\u3063\u3071\u3070\u308a\u30e0\u30ba\u3044 #2"
    },
    {
        "channelId": "UCe_p3YEuYJb8Np0Ip9dk-FQ",
        "streamingNumber": "374\u4eba",
        "videoTitle": "\u3010\u5b9a\u671f\u30e9\u30b8\u30aa\u3011\u3042\u30fc\u3053\u306e\u30ef\u30f3\u30ca\u30a4\u30c8\u30b8\u30e3\u30c3\u30dd\u30f3\uff0306\u3010\u306b\u3058\u3055\u3093\u3058/\u671d\u65e5\u5357\u30a2\u30ab\u30cd\u3011"
    },
    {
        "channelId": "UC6oDys1BGgBsIC3WhG1BovQ",
        "streamingNumber": "2220\u4eba",
        "videoTitle": "\ud83d\udd3408:\u3010HITMAN\u3011\u65b0\u4eba\u6697\u6bba\u8005\u306e\u4eca\u9031\u3082\u304a\u75b2\u308c\u69d8\u91d1\u66dc\u65e5\uff01\u3010\u306b\u3058\u3055\u3093\u3058/\u9759\u51db\u3011"
    },
    {
        "channelId": "UCryOPk2GZ1meIDt53tL30Tw",
        "streamingNumber": "970\u4eba",
        "videoTitle": "\ud83d\uded1\u3010\u97f3\u30d5\u30a7\u30c1/Binaural\u3011\u6700\u9ad8\u306e\u97f3\u3092\u805e\u304f\u591c\u306e\u304a\u3068\u3042\u305d\u3073 \u30aa\u30ce\u30de\u30c8\u30da\u7de8 2020.10.3\u3010\u306b\u3058\u3055\u3093\u3058/\u9234\u6728\u52dd\u3011"
    },
    {
        "channelId": "UC_BlXOQe5OcRC7o0GX8kp8A",
        "streamingNumber": "443\u4eba",
        "videoTitle": "\u3010Apex\u3011\u6226\u5834\u306b\u99c6\u3051\u308b\u72ac\u3010\u7fbd\u67f4\u306a\u3064\u307f / \u3042\u306b\u307e\u30fc\u308c\u3011"
    },
    {
        "channelId": "UCvmppcdYf4HOv-tFQhHHJMA",
        "streamingNumber": "576\u4eba",
        "videoTitle": "\u5973\u795e\u3068\u65c5\u3059\u308b\u5927\u795e\u3000\u305d\u306e4"
    },
    {
        "channelId": "UCUZ5AlC3rTlM-rA2cj5RP6w",
        "streamingNumber": "5554\u4eba",
        "videoTitle": "\u3010\u30af\u30e9\u30d5\u30c8\u30d4\u30a2\u3011\u307e\u3063\u305f\u304f\u77e5\u3089\u306a\u304f\u3066\u3082\u697d\u3057\u3044\u3089\u3057\u3044\u30b2\u30fc\u30e0"
    },
    {
        "channelId": "UCmovZ2th3Sqpd00F5RdeigQ",
        "streamingNumber": "6171\u4eba",
        "videoTitle": "\u3010\u30d1\u30ef\u30d7\u30ed2020\u6804\u51a0\u30ca\u30a4\u30f3\u3011\u4e8c\u5e74\u76ee\u3001\u5929\u624d\u3001\u964d\u81e8\u3002\u3010\u52a0\u8cc0\u7f8e\u30cf\u30e4\u30c8/\u306b\u3058\u3055\u3093\u3058\u3011"
    },
    {
        "channelId": "UCUKD-uaobj9jiqB-VXt71mA",
        "streamingNumber": "1\u4e07\u4eba",
        "videoTitle": "\u3010\u30de\u30a4\u30af\u30e9\u3011\u30d3\u30eb\u30b8\u30f3\u30b0\u5b8c\u6210\u306b\u5411\u3051\u3066\u5efa\u7bc9\u3092\u958b\u59cb\u3059\u308b\u56de\u3010\u7345\u767d\u307c\u305f\u3093/\u30db\u30ed\u30e9\u30a4\u30d6\u3011"
    },
    {
        "channelId": "UCL4gvO_wg0SA-ecWiVKN-MQ",
        "streamingNumber": "33\u4eba",
        "videoTitle": "[MHW:IB]\u30de\u30eb\u30c1\u3067\u52dd\u3061\u305f\u3044\u30df\u30e9\u30dc\u30ec\u30a2\u30b9[\u958b\u653e\u578b]"
    },
    {
        "channelId": "UCq8u9iiEXAWPqFiI93is8qg",
        "streamingNumber": "30\u4eba",
        "videoTitle": "\u4f5c\u696d\u54e1\uff08\u6751\u4eba\uff09\u7528\u30db\u30c6\u30eb\u3092\u4f5c\u308b\uff16\u3000\u30de\u30a4\u30af\u30e9\u7dcf\u5408\u7248"
    },
    {
        "channelId": "UC_a1ZYZ8ZTXpjg9xUY9sj8w",
        "streamingNumber": "9633\u4eba",
        "videoTitle": "\u3010\u30b9\u30fc\u30d1\u30fc\u30de\u30ea\u30aa35\u3011\u79c1\u306f\u3069\u3053\u307e\u3067\u751f\u304d\u6b8b\u308c\u308b\u304b\u2026\uff01\uff01\u3010\u9234\u539f\u308b\u308b/\u306b\u3058\u3055\u3093\u3058\u3011"
    },
    {
        "channelId": "UC1opHUrw8rvnsadT-iGp7Cg",
        "streamingNumber": "2.3\u4e07\u4eba",
        "videoTitle": "\u3010Minecraft\u3011\u30c9\u30ad\u30c9\u30ad\u30c3\uff01\u6df1\u591c\u306e\u30db\u30ed\u9bd6New\u30c9\u30c3\u30ad\u30ea\u8a08\u753b\uff01\uff01+\u03b1\u3010\u6e4a\u3042\u304f\u3042/\u30db\u30ed\u30e9\u30a4\u30d6\u3011"
    },
    {
        "channelId": "UC8L07dTOhR4-uOXTbIDWEnQ",
        "streamingNumber": "162\u4eba",
        "videoTitle": "\u3010\u539f\u795e/genshin\u3011\u30c8\u30ef\u30ea\u30f3\u3092\u6551\u3044\u305f\u3044\u3000#3\u3010VTuber\u7345\u5802\u30ea\u30aa\u3011"
    },
    {
        "channelId": "UCTIE7LM5X15NVugV7Krp9Hw",
        "streamingNumber": "2277\u4eba",
        "videoTitle": "\u3010\u30b9\u30fc\u30d1\u30fc\u30de\u30ea\u30aa\u30b5\u30f3\u30b7\u30e3\u30a4\u30f3\u3011\uff0302 \u5168\u7802\u6d5c\u306b\u6c34\u3092\u6492\u304f\u914d\u7ba1\u5de5\u3010\u306b\u3058\u3055\u3093\u3058/\u5922\u8ffd\u7fd4\u3011Super Mario Sunshine"
    },
    {
        "channelId": "UCFKOVgVbGmX65RxO3EtH3iw",
        "streamingNumber": "1.2\u4e07\u4eba",
        "videoTitle": "\u3010Minecraft\u3011\u306d\u307d\u3089\u307c\u30d3\u30eb\u5efa\u8a2d\uff01\u4eee\u571f\u53f0\u3092\u4f5c\u308a\u307e\u3059\u3010\u96ea\u82b1\u30e9\u30df\u30a3/\u30db\u30ed\u30e9\u30a4\u30d6\u3011"
    },
    {
        "channelId": "UChAnqc_AY5_I3Px5dig3X1Q",
        "streamingNumber": "6633\u4eba",
        "videoTitle": "\u3010\u30b9\u30d1\u30c1\u30e3\u306e\u304a\u793c\u306a\u3069\u3011\u304a\u8a95\u751f\u65e5\u4f1a\u305f\u306e\u3057\u304b\u3063\u305f\uff08\u5f8c\u591c\u796d\uff09\u3010\u30db\u30ed\u30e9\u30a4\u30d6/\u620c\u795e\u3053\u308d\u306d\u3011"
    }
]

with open(settings.streamingDataPath(), "r") as f:
    streamingData = json.load(f)

streamingDataNew = []

for strDa in streamingData:
    if strDa["channelId"] in str(streamingChannels): # 既存のデータが新規のデータに含まれていた場合
        channelId       = strDa["channelId"]
        streamingNumber = strDa["streamingNumber"]
        videoTitle      = strDa["videoTitle"]
        print("既存：",channelId)
        streamingDataNew.append({"channelId": channelId, "streamingNumber": streamingNumber, "videoTitle": videoTitle}) # 既存ライバー追加

for strCha in streamingChannels:
    if strCha["channelId"] not in str(streamingData): # 書き込み用データにまだ含まれていない場合
        channelId       = strCha["channelId"]
        streamingNumber = strCha["streamingNumber"]
        videoTitle      = strCha["videoTitle"]
        print("配信開始：",channelId)
        streamingDataNew.append({"channelId": channelId, "streamingNumber": streamingNumber, "videoTitle": videoTitle}) # 開始ライバー追加
