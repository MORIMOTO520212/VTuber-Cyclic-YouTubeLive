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
    try:
        resp = requests.get('https://idtwi.com/search/'+twitterId)
        soup = BeautifulSoup(resp.text, 'html.parser')
        dd = soup.find_all('dd')[1]
        twitterUserId = dd.find('a').text
        twitterUserId = twitterUserId.replace(' (1)', '')
    except Exception as e:
        print(str(e))
        return False
    return twitterUserId

# ユーザーID → TwitterID 変換
def searchTwitterId(twitterUserId):
    # idtwi.comからスクレイピング
    try:
        resp = requests.get('https://idtwi.com/'+twitterUserId)
        soup = BeautifulSoup(resp.text,'html.parser')
        twitterId = soup.find_all('b')[0].text
    except Exception as e:
        print(str(e))
        return False
    return twitterId