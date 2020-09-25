from selenium import webdriver
from selenium.webdriver.firefox.options import Options

fp = webdriver.FirefoxProfile('C:\\Users\\kante\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\so4o45dh.default')
#Options.profile('C:\\Users\\kante\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\so4o45dh.default')
Options.set_headless()
browser = webdriver.Firefox(fp, firefox_options=Options)

browser.get('https://www.youtube.com/feed/subscriptions')