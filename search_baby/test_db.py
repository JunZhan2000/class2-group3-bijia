from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import mysql.connector
import requests
from lxml import etree
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



def judge():
    search_baby = '宝宝你好'
    url = 'http://search.dangdang.com/?key=' + search_baby + '&page_index=1'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
    }
    res = requests.get(url, headers=headers)
    selector = etree.HTML(res.text)

    links = selector.xpath('//ul[@class="bigimg"]/li')
    sell_numlinks = selector.xpath('//p[@class="search_star_line"]/a/text()')
    print(len(links))
    for i in range(0, len(links)):
        '''一次循环读取并提交一个商品'''
        name = links[i].xpath('a/@title')[0]
        url = links[i].xpath('a/@href')[0].replace('//', '')
        sell_num = sell_numlinks[i].replace('条评论', '')
        try:
            img_adress = links[i].xpath('a/img/@data-original')[0]
            img_adress = img_adress.replace('//', '')
        except:
            img_adress = links[i].xpath('a/img/@src')[0]

        try:
            price = links[i].xpath('p[3]/span[1]/text()')[0].replace('¥', '')
            #     print(price)
        except:
            price = links[i].xpath('div[2]/p[2]/span/text()')[0].replace('¥', '')
        # """下面是获得商铺名字，判断是否自营"""
        try:
            shop_name = links[i].xpath('p[@class="search_shangjia"]/a/@title')[0]
            #     print(shop_name)
            if_official = False
        except:  ##否则就是当当自营
            shop_name = '当当自营'
            #     print(shop_name)
            if_official = True
        ds_name = '当当'
        show_baby_list(url=url, name=name, shop_name=shop_name, ds_name=ds_name,
                    img_adress=img_adress, price=price ,if_official=if_official, sell_num=sell_num)
        img_adress2 = 'http://img3m4.ddimg.cn/26/18/27865754-1_b_10.jpg'
        url2 = 'http:product.dangdang.com/27865754.html'
        name2 = ' 宝宝，你好！成长绘本'
        shop_name2 = '当当自营'
        ds_name2 = '当当'
        price2 = '268.90'
        sell_num2 = '9'
        if_official2 = True

        if img_adress == img_adress2:
            print(1)
        if url == url2:
            print(2)
        if name == name2:
            print(3)
        if shop_name == shop_name2:
            print(4)
        if ds_name == ds_name2:
            print(5)
        if price == price2:
            print(6)
        if sell_num == sell_num2:
            print(7)
        if if_official == if_official2:
            print(8)



        if i == 0:
            return


judge()