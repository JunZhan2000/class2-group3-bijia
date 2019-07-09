import requests
from lxml import etree
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



# # 创建对象的基类:
# Base_db = declarative_base()

# # 定义Baby对象:
# class Babies(Base_db):
#     '''
#     商品表
#     商品图片地址：img_adress　　　商品地址：url
#     商品名：name　　　电商名：ds_name
#     店铺名：shop_name　　　是自营还是第三方：if_official，为１则是自营店，为０则是第三方店铺
#     价格: price　　　销量：sell_num'''
    
#     # 表的名字:
#     __tablename__ = 'babies'
#     id = Column(Integer, primary_key=True)  # 主键
#     name = Column(String)  # 商品名
#     price = Column(String)  # 商品价格
#     sell_num = Column(String)  # 销量
#     url = Column(String, unique=True)  # 商品链接
#     img_adress = Column(String)  # 图片链接
#     shop_name = Column(String)  # 店铺名
#     ds_name = Column(String)  # 电商名
#     if_official = Column(String)  # 是自营店还是第三方




# # 初始化数据库连接:
# engine = create_engine('mysql+mysqlconnector://root:!pplxy2233..!1lb;@localhost:3306/bijia')
# # '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
# # 创建DBSession类型:
# DBSession = sessionmaker(bind=engine)





# img_adress2 = 'http://img3m4.ddimg.cn/26/18/27865754-1_b_10.jpg'
# url2 = 'http:product.dangdang.com/27865754.html'
# name2 = ' 宝宝，你好！成长绘本'
# shop_name2 = '当当自营'
# ds_name2 = '当当'
# price2 = '268.90'
# sell_num2 = '9'
# if_official2 = True



# a_baby = Babies(img_adress=img_adress2, url=url2, name=name2, shop_name=shop_name2, ds_name=ds_name2,
# price=price2, sell_num=sell_num2, if_official=if_official2)


# # 创建session对象:
# session = DBSession()
# session.add(a_baby)
# print('222\n333')
# session.commit()
# # 关闭Session:
# session.close()




# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:!pplxy2233..!1lb;@localhost:3306/bijia')
# '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

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
# 创建Baby实例并提交
a_baby = Babies(name=name, url=url, sell_num=sell_num, shop_name=shop_name,
img_adress=img_adress, ds_name='当当网', price=price, if_official=if_official)
show_baby_list(name=a_baby.name, url=a_baby.url, sell_num=a_baby.sell_num, shop_name=a_baby.shop_name, 
            img_adress=a_baby.img_adress, ds_name=a_baby.ds_name, price=a_baby.price, if_official=a_baby.if_official)
session.add(a_baby)
# 提交会话
session.commit()
# 关闭Session:
session.close()

