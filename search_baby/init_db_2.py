from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import mysql.connector
from init_db import Babies
import requests
from lxml.html import etree


# 创建对象的基类:
Base_db = declarative_base()

# 定义Baby对象:
class Babies(Base_db):
    '''
    商品表
    商品图片地址：img_adress　　　商品地址：url
    商品名：name　　　电商名：ds_name
    店铺名：shop_name　　　是自营还是第三方：if_official，为１则是自营店，为０则是第三方店铺
    价格: price　　　销量：sell_num'''
    
    # 表的名字:
    __tablename__ = 'babies'
    id = Column(Integer, primary_key=True)  # 主键
    name = Column(String)  # 商品名
    price = Column(String)  # 商品价格
    sell_num = Column(String)  # 销量
    url = Column(String, unique=True)  # 商品链接
    img_adress = Column(String)  # 图片链接
    shop_name = Column(String)  # 店铺名
    ds_name = Column(String)  # 电商名
    if_official = Column(String)  # 是自营店还是第三方



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


# def search_dd(search_baby):
#     """下面是获得当当宝贝的信息
#     输入想要的商品，输入商品列表"""
    
search_baby='宝宝你好'
headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
}

url = 'http://search.dangdang.com/?key=' + search_baby + '&page_index=1'
 
res = requests.get(url, headers=headers)
selector = etree.HTML(res.text)

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:!pplxy2233..!1lb;@localhost:3306/bijia')
# '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()
img_adress = selector.xpath('//*[@id="p27865754"]/a/img//@src')[0]
name = selector.xpath('//*[@id="p27865754"]/p[1]/a//@title')[0]
url = selector.xpath('//*[@id="p27865754"]/p[1]/a//@href')[0]
# sell_num = selector.xpath('//*[@id="p26512518"]/div[1]/span/span[1]/')[0].text
# shop_name = selector.xpath('//*[@id="p27865754"]/div[1]/span/span[1]/')[0].text
sell_num = '3'
shop_name = '当当自营'
ds_name = '当当'
price = selector.xpath('//*[@id="p27865754"]/p[3]/span[2]/text()')[0]
if_official = True

name = str(name)
img_adress = str(img_adress)
url = str(url)
price = str(price)



# 创建Baby实例并提交
a_baby = Babies(name=name, url=url, sell_num=sell_num, shop_name=shop_name,
                    img_adress=img_adress, ds_name='当当网', price=price, if_official=if_official)
show_baby_list(name=a_baby.name, url=a_baby.url, sell_num=a_baby.sell_num, shop_name=a_baby.shop_name, 
        img_adress=a_baby.img_adress, ds_name=a_baby.ds_name, price=a_baby.price, if_official=a_baby.if_official)



session.add(a_baby)
# 提交会话
session.commit()
print('111\n')
# 关闭Session:
session.close()