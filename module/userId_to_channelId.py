# userId_to_channelId.py
# create: 2022.01.16
# author: YUMA.morimoto
# description: 

import re, requests


def convert_channelId(user_id):
    'ユーザーIDからチャンネルIDに変換する。\
    user_id = \'/c/SunadaZenon\''
    try:
        resp = requests.get('https://www.youtube.com'+user_id)
        res = re.findall('\"browse_id\",\"value\":\".{24}', resp.text)[0]
        channel_id = res[-24:]
        return channel_id
    except:
        return False