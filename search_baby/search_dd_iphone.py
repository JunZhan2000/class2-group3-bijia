import re
import requests
from bs4 import BeautifulSoup
from lxml import etree
from multiprocessing import Pool
from init_db import DBSession, Babies
# import pymongo
import time

# client = pymongo.MongoClient('localhost',27017)
# project = client['project']
# dd_baby = project['dd_baby']

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
    print('%s' % price)
    print('销量：')
    print('%s' % sell_num)
    print('是否自营：')
    print('%s' % if_official)
    print('\n')
def search_dd(search_baby):
    """下面是获得当当宝贝的信息
    输入想要的商品，输入商品列表"""
    for i in range(1,10):
        url = 'http://search.dangdang.com/?key='+search_baby+'&page_index={}'.format(str(i))
        compile_url(url)
        print("第%d页" % i)
        time.sleep(2)
def compile_url(url):
    """下面是获得网址
    获得商品  将商品打包成字典
    添加商品到商品列表内
    """
    headers = {
     'User-Agent': 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
    }
    # 创建session对象:
    session = DBSession()
    res = requests.get(url,headers=headers)
    selector = etree.HTML(res.text)
    test_if = '【当当自营】'
    test_If = '当当自营'
    links = selector.xpath('//ul[@class="bigimg cloth_shoplist"]/li')
    number = 0
    for link in links:
        number += 1
        name = link.xpath('a/@title')[0]
        url = link.xpath('a/@href')[0].replace('//','')
        img_adress = link.xpath('a/img/@src')[0]  
        price = link.xpath('p[@class="price"]/span[1]/text()')[0]
        #"""下面是获得商铺名字，判断是否自营"""
        shop_name = link.xpath('p[@class="link"]/a/text()')[0]
        # 将商品信息由__elementunicoderesult类型转成string类型
        url = str(url)
        name = str(name)
        shop_name = str(shop_name)
        img_adress = str(img_adress)
        price = str(price)
        ds_name = str('当当网')
        if test_if in name or test_If in shop_name:
            if_official = 1
        else:
            if_official = 0
    ##下面是获取评论数
        sell_num = link.xpath('p[@class="star"]/a/text()')[0]
        sell_num = str(sell_num)
        print(str(number) +':')
        show_baby_list(url=url, name=name, shop_name=shop_name, ds_name=ds_name,
                       img_adress=img_adress, price=price ,if_official=if_official, sell_num=sell_num)
        # 创建Baby实例并提交
        a_baby = Babies(name=name, url=url, sell_num=sell_num, shop_name=shop_name,
                      img_adress=img_adress, ds_name='当当网', price=price, if_official=if_official)
        session.add(a_baby)
    session.commit()
    # 关闭Session:
    session.close()
search_dd('手机')