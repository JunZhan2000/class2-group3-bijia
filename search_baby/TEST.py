import csv
import re
import requests
from bs4 import BeautifulSoup
from lxml import etree
import time
from selenium import webdriver
import pymongo

client = pymongo.MongoClient('localhost',27017)
project = client['project']
baby_price = project['baby_price']
driver = webdriver.Chrome()
driver.maximize_window()

fp = open('C:/Users/Administrator/Desktop/test.csv')
reader = csv.reader(fp)
number = 0
headers = {
     'User-Agent': 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
}
def compile_url(url):
    driver.get(url)
    driver.implicitly_wait(30)  # 隐式等待30s
    time.sleep(1)  # 等待页面加载完，注意观察滚动条目前处于最上方
    res = driver.page_source  ##获取页面信息
    selector = etree.HTML(res)  # 进行解析
    try:
        price = selector.xpath('//span[@class="mainprice"]/text()')[0].replace('.','')+'.00'
    except:
        price = ''
    baby_price.insert({'price':price})
for row in reader:
    number += 1
    row = 'http://'+ row[0]
    print(row)
    compile_url(row)
    print("第%d页" % number)
fp.close()