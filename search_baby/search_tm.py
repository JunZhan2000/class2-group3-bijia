#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import asyncio
import time
import random
from pyppeteer.launcher import launch   # 控制模拟浏览器用
from retrying import retry      # 设置重试次数用的
import re
from bs4 import BeautifulSoup
from lxml import etree
from init_db import DBSession, Babies

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
async def main(username, pwd, url,search_baby,list_page,loop): # 定义main协程函数，
    # dumpio:true 浏览器就不会卡住了
    browser = await launch({'headless': False, 'userDataDir':r'F:\Temporary','args': ['--no-sandbox'], 'dumpio':True})     # 启动pyppeteer 属于内存中实现交互的模拟器
    page = await browser.newPage()   # 启动个新的浏览器页面
    await page.setExtraHTTPHeaders({
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
    })
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) chrome/72.0.3626.109 Safari/537.36')
    await page.goto(url)# 访问登录页面
    await page_evaluate(page)
    await page.waitFor(2)
    await spider_search(browser, page,search_baby,list_page)
    print('over')
    await page.close()
    #time.sleep(10)
    await browser.close()

async def page_evaluate(page):
    # 替换淘宝在检测浏览时采集的一些参数。
    # 就是在浏览器运行的时候，始终让window.navigator.webdriver=false
    # navigator是window对象的一个属性，同时修改plugins，languages，navigator
    await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => undefined } }) }''')  # 以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果。
    await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')
# async def spider_compile(url,page):
#     links =await page.xpath('//*[@id="mainsrp-itemlist"]/div/div/div[1]/div[{}]/div[1]/div/div[1]'.format(i) for i in range(44))
#     for link in links:
#         href =

async def spider_parser(res):
    '''用于解析一个网址的html'''
    #创建session对象:
    session = DBSession()
    selector = etree.HTML(res)
    number = 0 
    ##名字  图片地址  地址
    ##销量  商店名字  电商  是否自营 价格
    # # 获取每个商品的八个属性，包括商品名字，价格，销量，地址，图片地址，电商, 商店名字，是否为自营
    ##获取大标签
    links = selector.xpath('//div[@id="J_ItemList"]/div/div')
    for link in links:
        ##下面测试获取网址和图片网址
        number += 1
        url = link.xpath('div[1]/a/@href')[0].replace('//','')
        img_adress = link.xpath('div[@class="productImg-wrap"]/a/img/@src')[0].replace('//','')
        price = link.xpath('p[1]/em/text()')[0]
        # try:
        #     name = link.xpath('p[@class="productTitle"]/a[1]/span/text()[1]')[0]+link.xpath('p[@class="productTitle"]/a[1]/text()[2]')[0]
        # except:
        #     name = link.xpath('p[@class="productTitle"]/a[1]/text()[1]')[0]
        name = link.xpath('p[@class="productTitle"]/a[1]/@title')[0]
        name = name.strip()
        '''自定义电商名'''
        ds_name = '天猫商城'
        '''下面测试获得销量'''
        try:
            sell_num = link.xpath('p[@class="productStatus"]/span[1]/em[1]/text()')[0].replace('笔','')
        except:
            sell_num = '0'
        '''下面获取商铺名'''
        try:
            shop_name = link.xpath('div[@class="productShop"]/a[1]/span/text()')[0].strip() + link.xpath('div[@class="productShop"]/a[1]/text()[2]')[0].strip()
        except:
            shop_name = link.xpath('div[@class="productShop"]/a[1]/text()')[0].strip()
        '''下面看是否自营'''
        if '官方' in shop_name:
            if_official = True
        else:
            if_official = False
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
        print(str(number) +':')
        if shop_name != '苏宁易购官方旗舰店' and len(name)!= 0 and price>500 :
            show_baby_list(url=url, name=name, shop_name=shop_name, ds_name=ds_name,img_adress=img_adress, price=price ,if_official=if_official, sell_num=sell_num)
            # 创建Baby实例并提交
            a_baby = Babies(name=name, url=url, sell_num=sell_num, shop_name=shop_name,
                     img_adress=img_adress, ds_name='天猫商城', price=price, if_official=if_official)
            session.add(a_baby)
        else:
            pass
    session.commit()
    #关闭Session:
    session.close()

async def spider_search(browser, page,search_baby,list_page):
    url = 'https://list.tmall.com/search_product.htm?q='+search_baby+'&s=0'
    await page.goto(url)
    await page_evaluate(page)
    contents = []
    cur_dist = 0
    height = await page.evaluate("() => document.body.scrollHeight")
    while True:
        if cur_dist < height:
            await page.evaluate("window.scrollBy(0, 500);")
            await asyncio.sleep(0.5)
            cur_dist += 500
        else:
            break
    # res =await page.content()
    # contents.append(res)
    # await spider_parser(res)#获得页面内容
    page_num = 0
    while page_num < list_page:
        print(page_num+1)
        time.sleep(2)
        # 这里选择通过构造url来翻页，这样对于可能出现的滑块验证就存在于page中
        # 如果选择通过点击页面的翻页按钮翻页，则会在当前页面弹出一个小框滑动验证，此时需要检查页面的frames,找到弹出的框才能定位到滑块
        url = 'https://list.tmall.com/search_product.htm?q='+search_baby+'&s={}'.format(60*page_num)
        await page.goto(url)
        # 由于重新跳转了页面，window.navigator.webdriver的值被改为了true，需要再次设置为undefined，否则翻页过程中出现滑块，则会一直滑动失败
        await page_evaluate(page)
        height = await page.evaluate("() => document.body.scrollHeight")
        cur_dist = 0
        while True:
            if cur_dist < height:
                await page.evaluate("window.scrollBy(0, 500);")
                await asyncio.sleep(0.5)
                cur_dist += 500
            else:
                break
        res = await page.content()
        contents.append(res)
        await spider_parser(contents[page_num])
        try:
            slider = await page.Jeval('#nocaptcha', 'node => node.style')  # 是否有滑块
            if slider:
                while True:
                    print('刷新')
                    # 用于滑动失败刷新
                    flag, page = await mouse_slide(page=page)
                    fresh = ''
                    try:
                        fresh = await page.Jeval('.errloading', 'node => node.textContent')
                    except:
                        pass
                    if fresh:
                        await page.hover('a[href="javascript:noCaptcha.reset(1)"]')
                        await page.mouse.down()
                        await page.mouse.up()
                        time.sleep(1)
                    else:
                        break
            else:
                await page.hover('a[href="javascript:noCaptcha.reset(1)"]')
                await page.mouse.down()
                await page.mouse.up()
                time.sleep(1)
        except Exception as e:
            print(e)
            pass
        page_num += 1
    print('over')

# 获取登录后cookie
async def get_cookie(page):
    cookies_list = await page.cookies()
    cookies = ''
    for cookie in cookies_list:
        str_cookie = '{0}={1};'
        str_cookie = str_cookie.format(cookie.get('name'), cookie.get('value'))
        cookies += str_cookie
    return cookies


def retry_if_result_none(result):
    return result is None


@retry(retry_on_result=retry_if_result_none,)
async def mouse_slide(page=None, frame=None):
    await asyncio.sleep(2)
    try:
        # 鼠标移动到滑块，按下，滑动到头（然后延时处理），松开按键
        if frame:
            await frame.hover('#nc_1_n1z')
        else:
            await page.hover('#nc_1_n1z')
        await page.mouse.down()
        await page.mouse.move(2000, 0,{'delay': random.randint(1000, 2000)}) 
        await page.mouse.up()
    except Exception as e:
        print(e, ':验证失败')
        return None, page
    else:
        await asyncio.sleep(2)
        # 判断是否通过
        slider_again = ''
        try:
            slider_again = await page.Jeval('.nc-lang-cnt', 'node => node.textContent')
        except:
            pass
        if slider_again != '验证通过':
            return None, page
        else:
            print('验证通过')
            return 1, page


def input_time_random():
    return random.randint(100, 151)


# if __name__ == '__main__':
def search_tm(search_baby,page):
    username = ''   # 淘宝用户名
    pwd = ''  # 密码
    url = 'https://login.tmall.com/'
    loop = asyncio.get_event_loop()  # 协程，开启个无限循环的程序流程，把一些函数注册到事件循环上。当满足事件发生的时候，调用相应的协程函数。
    m = main(username, pwd, url,search_baby,page,loop=loop)
    loop.run_until_complete(m)  # 将协程注册到事件循环，并启动事件循环
def search5():
    # search_tm('华为手机',10)
    # search_tm('iphone',10)
    # search_tm('oppo手机',10)
    # search_tm('vivo手机',2)
    # search_tm('小米手机',10)
    search_tm('魅族手机',10)
    search_tm('nubia手机',1)

search5()