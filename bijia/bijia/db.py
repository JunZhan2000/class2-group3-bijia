from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import mysql.connector



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

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:Zj20190901@localhost:3306/bijia')
# '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)