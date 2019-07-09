from time import sleep
from lxml import etree
from selenium import webdriver
from init_db import DBSession, Babies

# from selenium.webdriver.chrome.options import Options
# #这个是一个用来控制chrome以无界面模式打开的浏览器
# #创建一个参数对象，用来控制chrome以无界面的方式打开
# chrome_options = Options()
# #后面的两个是固定写法 必须这么写
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# #驱动路径 谷歌的驱动存放路径
# path = r'D:\\ANACONDA'
# #创建浏览器对象
# driver = webdriver.Chrome(executable_path=path,chrome_options=chrome_options)
driver = webdriver.Chrome()
driver.maximize_window()
def search_snyg(search_baby,page):
    '''爬取苏宁易购信息的总函数
    输入宝贝名search_baby,输出宝贝列表snyg_baby_list'''
    urls = Get_url(search_baby,page)
    '''对每个url进行爬取信息'''
    for url in urls:
        search_a_url(url)

def Get_url(baby,page):  # 定义下一页函数
    urls = []
    for i in range(page):
        url ='https://search.suning.com/' + baby + '/&iy=0&isNoResult=0&cp='+str(i)
        urls.append(url)
    return urls
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
        js = 'window.scrollBy(0,900)'
        driver.execute_script(js)
        driver.implicitly_wait(30)
        sleep(1)
    res = driver.page_source  ##获取页面信息
    selector = etree.HTML(res)  # 进行解析
    number = 0
    ##名字  图片地址  地址
    ##销量  商店名字  电商  是否自营 价格
    # # 获取每个商品的八个属性，包括商品名字，价格，销量，地址，图片地址，电商, 商店名字，是否为自营
    links = selector.xpath('//ul[@class="general clearfix"]/li/div/div')
    for link in links:
        number = number + 1
        if len(link.xpath('div[2]/div[3]/em/text()')) != 0:
            pass
        else:
            try:
                price = link.xpath('div[2]/div[1]/span[1]/text()[2]')[0] 
            except:
                price = link.xpath('div[2]/div[1]/span[1]/text()[1]')[0]
            if len(price) == 0 :
                pass
            else:
                price = price +'.00'
            ds_name = '苏宁易购'
            ##下面是店铺名称和是否自营
            shop_name = link.xpath('div[2]/div[4]/a[1]/text()')[0]
            if '苏宁' in shop_name:
                if_official = True
            else:
                if_official = False
            name = link.xpath('div[1]/div[1]/a/img/@alt')[0]
            img_adress = link.xpath('div[1]/div[1]/a/img/@src')[0].replace('//','')
            url = link.xpath('div[1]/div[1]/a/@href')[0].replace('//','')
            ##下面是获取销量
            try:
                sell_num = link.xpath('div[2]/div[3]/div/a/i/text()')[0].replace('+','')
            except:
                sell_num = '0'
            url = 'http://'+str(url)
            name = str(name)
            shop_name = str(shop_name)
            img_adress = 'http://'+str(img_adress)
            price = float(str(price))
            try:
                sell_num = int(str(sell_num))
            except:
                if '.' in sell_num:
                    sell_num = float(str(sell_num).replace('万','0'))
                    sell_num = int(sell_num*10000)
                else:
                    sell_num = float(str(sell_num).replace('万','0'))
                    sell_num = int(sell_num*1000)
            print(str(number)+':')
            if price!= 0 and price>500 :
                show_baby_list(url=url, name=name, shop_name=shop_name, ds_name=ds_name,
                            img_adress=img_adress, price=price ,if_official=if_official, sell_num=sell_num)
                # 创建Baby实例并提交
                a_baby = Babies(name=name, url=url, sell_num=sell_num, shop_name=shop_name,
                            img_adress=img_adress, ds_name=ds_name, price=price, if_official=if_official)
                session.add(a_baby)
            else: 
                pass
    session.commit()
    # 关闭Session:
    session.close()
def search3():
    search_snyg('华为手机',25)
    search_snyg('iphone手机',7)
    search_snyg('oppo手机',2)
    search_snyg('vivo手机',3)
    search_snyg('小米手机',3)
    search_snyg('魅族手机',3)
search3()