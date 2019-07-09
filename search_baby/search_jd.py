import re
from lxml import etree
from time import sleep
import requests
from selenium import webdriver
from init_db import DBSession, Babies
# import pymongo
import time

driver = webdriver.Firefox()
driver.maximize_window()
def Get_url(baby,page): #得到urls
    urls = []
    for i in range(page):
        url = 'https://search.jd.com/Search?keyword='+baby+'&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&page='+str(2*i)+'&s=107&click=0'
        urls.append(url)
    return urls

def search_jd(search_baby,page):
    '''爬取苏宁易购信息的总函数
    输入宝贝名search_baby,输出宝贝列表snyg_baby_list'''
    urls = Get_url(search_baby,page)
    '''对每个url进行爬取信息'''
    for url in urls:
        search_a_url(url)

def show_baby_list(img_adress, url, name, shop_name, ds_name, price, sell_num, if_official):
    '''格式化输出baby_list'''
    print('图片地址：')
    print('%s' % img_adress)
    print('宝贝地址：')
    print('%s' % url)
    print('宝贝名：')
    print('%s' % name)
    print('店铺名：')
    print('%s' % shop_name)
    print('电商名：')
    print('%s' % ds_name)
    print('宝贝价格：')
    print('%s' % str(price))
    print('销量：')
    print('%s' % str(sell_num))
    print('是否自营：')
    print('%s' % str(if_official))
    print('\n')
def search_a_url(url):
    '''用于解析一个网址的html
    输入url,返回宝贝列表a_baby_list'''
     # 创建session对象:
    session = DBSession()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) chrome/72.0.3626.109 Safari/537.36'
    }
    driver.get(url)
    driver.implicitly_wait(30)  # 隐式等待30s
    sleep(2)  # 等待页面加载完，注意观察滚动条目前处于最上方
    for i in range(15):
        js = 'window.scrollBy(0,360)'
        driver.execute_script(js)
        driver.implicitly_wait(30)
        sleep(0.5)
    res = driver.page_source  ##获取页面信息
    selector = etree.HTML(res)  # 进行解析
    number = 0
    ##名字  图片地址  地址
    ##销量  商店名字  电商  是否自营 价格
    # # 获取每个商品的八个属性，包括商品名字，价格，销量，地址，图片地址，电商, 商店名字，是否为自营
    ##获取大标签
    links = selector.xpath('//*[@id="J_goodsList"]/ul/li/div')
    ##下面测试获取名字
    prices = links[0].xpath('//div[3]/strong/i/text()')
    for link in links:
        price = prices[number]
        number += 1
        name1 = link.xpath('div[4]/a/em/text()[1]')
        name2 = link.xpath('div[4]/a/em/text()[2]')
        name = name1+name2
        try:
            name = name[0]+name[1]
        except:
            name = name[0]
        '''下面测试获得销量'''
        sell_num = link.xpath('div[5]/strong/a/text()')[0].replace('+','')
        
        '''下面获取商品地址和图片地址'''
        url = link.xpath('div[1]/a/@href')[0].replace('//', '')
        img_adress = link.xpath('div[1]/a/img/@src')[0].replace('//', '')
        '''自定义电商名'''
        ds_name = '京东商城'
        '''下面获取商铺名'''
        try:
            shop_name = link.xpath('div[7]/span/a/text()')[0]
        except:
            shop_name = ''
        '''下面看是否自营'''
        try:
            official = link.xpath('div[8]/i[1]/text()')[0]
            if official == '自营':
                if_official= True
            else:
                if_official= False
        except:
            if_official= 0
        url ='http://'+ str(url)
        name = str(name)
        shop_name = str(shop_name)
        img_adress = 'http://'+ str(img_adress)
        price = float(str(price))
        try:
            sell_num = int(str(sell_num))
        except:
            if '.' in sell_num:
                sell_num = float(str(sell_num).replace('万','0'))
                sell_num = sell_num*10000
            else:
                sell_num = float(str(sell_num).replace('万','0'))
                sell_num = sell_num*1000
        print(str(number) +':')
        if '二手' in name or price<500:
            pass
        else:
            show_baby_list(url=url, name=name, shop_name=shop_name, ds_name=ds_name,
                        img_adress=img_adress, price=price ,if_official=if_official, sell_num=sell_num)
            # 创建Baby实例并提交
            a_baby = Babies(name=name, url=url, sell_num=sell_num, shop_name=shop_name,
                        img_adress=img_adress, ds_name=ds_name, price=price, if_official=if_official)
            session.add(a_baby)
    session.commit()
    # 关闭Session:
    session.close()
    
def search2():
    search_jd('华为手机',18)  # 获取京东的宝贝列表
    search_jd('iphone',10)
    search_jd('oppo手机',4)
    search_jd('vivo手机',2)
    search_jd('小米手机',10)
    search_jd('魅族手机',6)
search2()