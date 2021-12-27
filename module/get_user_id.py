# get_user_id.py
# create: 2021.12.27
# author: YUMA.morimoto
# description: TwitterIDからユーザーIDを取得する。
#              これによりTwitterIDが変更されてもユーザーIDを使って新しいTwitterIDを探すことができる。

import requests
from bs4 import BeautifulSoup

# ユーザーIDを検索
def getTwitterUserId(twitterId):
    # idtwi.comからスクレイピング
    if not twitterId: # 引数に指定がなければFalse
        return False
    resp = requests.get("https://idtwi.com/search/"+twitterId)
    soup = BeautifulSoup(resp.text, 'html.parser')
    dd = soup.find_all('dd')[1]
    twitterUserId = dd.find('a').text
    twitterUserId = twitterUserId.replace(' (1)', '')
    return twitterUserId

# ユーザーIDを使ってTwitterIDを検索
def searchTwitterId(twitterUserId):
    