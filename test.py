from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep

Options = webdriver.FirefoxOptions()
# ヘッドレス
Options.headless = True
# 必須
Options.add_argument('--no-sandbox')
Options.add_argument('--disable-gpu')
# エラーの許容
Options.add_argument('--ignore-certificate-errors')
Options.add_argument('--allow-running-insecure-content')
Options.add_argument('--disable-web-security')
# headlessでは不要そうな機能
Options.add_argument('--disable-desktop-notifications')
Options.add_argument("--disable-extensions")
# UA設定（なくてもいい）
Options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0')
# 言語
Options.add_argument('--lang=ja')
# ユーザープロファイル
Options.profile = "myProfile"

driver = webdriver.Firefox(options=Options)
driver.get("http://www.example.com/")
print(str(driver.page_source))
print("successfully!")