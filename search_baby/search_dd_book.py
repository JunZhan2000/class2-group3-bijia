from init_db import DBSession, Babies
import requests
from lxml import etree
import time



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
    page_num = 5
    for i in range(1, page_num+1):
        url = 'http://search.dangdang.com/?key=' + search_baby + '&page_index={}'.format(str(i))
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
    res = requests.get(url, headers=headers)
    selector = etree.HTML(res.text)

    links = selector.xpath('//div[@dd_name="普通商品区域"]/ul/li')
    if not links:
        return
    sell_numlinks = selector.xpath('//p[@class="search_star_line"]/a/text()')

    # 创建session对象:
    session = DBSession()
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
        # 打印数据
        print(i)
        # 将商品信息由__elementunicoderesult类型转成string类型
        url = str(url)
        name = str(name)
        shop_name = str(shop_name)
        img_adress = str(img_adress)
        price = str(price)
        sell_num = str(sell_num)
        show_baby_list(url=url, name=name, shop_name=shop_name, ds_name=ds_name,
                       img_adress=img_adress, price=price ,if_official=if_official, sell_num=sell_num)
        # 创建Baby实例并提交
        a_baby = Babies(name=name, url=url, sell_num=sell_num, shop_name=shop_name,
                      img_adress=img_adress, ds_name='当当网', price=price, if_official=if_official)
        session.add(a_baby)
    session.commit()
    # 关闭Session:
    session.close()

search_dd('python入门')