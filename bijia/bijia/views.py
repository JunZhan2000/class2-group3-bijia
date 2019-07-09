from flask import redirect, url_for, render_template, request
from bijia import app
from bijia.forms import Search_bar, Price_set
import click
from bijia.func import zip_search_shop, get_search_shop, Result_url
from math import ceil
from bijia.get_data import get_baby_list





#　主页
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def hello_world():
    search_bar = Search_bar()
    # if request.method == 'POST' and search_bar.is_submitted():
    if search_bar.validate_on_submit():
        search_baby = search_bar.baby.data

        # 获取爬取数据的范围
        # 返回一个数字，转成二进制后的四位分别代表是否爬取淘宝京东苏宁易购当当
        ds_name_num = zip_search_shop(all=search_bar.all.data, taobao=search_bar.taobao.data, jingdong=search_bar.jingdong.data,
                                      suning=search_bar.suning.data, dangdang=search_bar.dangdang.data)

        # 重定向到搜索结果页面，同时传入宝贝名
        return redirect(url_for('search_result', search_baby = search_baby,
                                ds_name_num = ds_name_num))

    return render_template('index.html', form=search_bar)





#　显示宝贝搜索结果的页面
# @app.route('/search_result/<search_baby>/<int:search_shop>/<int:min_price>/<int:max_price>', defaults={
#                 'current_page': '1', 'sort_rule':'1'}, methods=['GET', 'POST'])
@app.route('/search_result/<search_baby>/<ds_name_num>', defaults={'current_page': '1',
                'sort_rule':'1', 'min_price': '-1', 'max_price': '0'}, methods=['GET', 'POST'])
@app.route('/search_result/<search_baby>/<ds_name_num>/<sort_rule>'
           '/<current_page>/<min_price>/<max_price>', methods=['GET', 'POST'])
def search_result(search_baby, ds_name_num, min_price='-1', max_price='0', sort_rule='1', current_page='1'):
    # 判定爬取的商城

    search_bar = Search_bar()    # 实例化搜索栏
    price_set = Price_set()    # 实例化价格筛选栏

    # 如果在搜索结果页面再次搜索
    if search_bar.validate_on_submit():
        search_baby = search_bar.baby.data
        # 获取爬取数据的范围
        # 返回一个数字，转成二进制后的四位分别代表是否爬取淘宝京东苏宁易购当当
        ds_name_num = zip_search_shop(all=search_bar.all.data, taobao=search_bar.taobao.data, jingdong=search_bar.jingdong.data,
                                      suning=search_bar.suning.data, dangdang=search_bar.dangdang.data)

        # 重定向到搜索结果页面，同时传入宝贝名
        return redirect(url_for('search_result',search_baby=search_baby, ds_name_num=ds_name_num))


    # 如果在搜索结果页面设置价格区间
    if price_set.validate_on_submit():
        click.echo(search_baby)
        click.echo(ds_name_num)
        min_price = price_set.min_price.data
        max_price = price_set.max_price.data
        return redirect(url_for('search_result',search_baby=search_baby, ds_name_num=ds_name_num,
        sort_rule=sort_rule, current_page=current_page, min_price=min_price, max_price=max_price))

    min_price = float(min_price)
    max_price = float(max_price)
    current_page = int(current_page)
    sort_rule = int(sort_rule)
    search_shop_dic = get_search_shop(ds_name_num)  # 电商字典
    search_shop = str(ds_name_num)

    # 检索数据库，获得五十个商品
    baby_list = get_baby_list(keyword=search_baby, search_shop_dic=search_shop_dic,
                sort_rule =sort_rule, min_price=min_price, max_price=max_price)
    all_pages = ceil(len(baby_list) / 10)  # 总页码数
    # 根据页码数切片，获得传给前端的十个商品
    start = (current_page-1) * 10
    final = start + 10
    baby_list = baby_list[start: final]


    for i in range(len(baby_list)):
        baby_list[i].price = str(baby_list[i].price)
        baby_list[i].sell_num = str(baby_list[i].sell_num)

    result_url = Result_url(search_baby=search_baby, ds_name_num=ds_name_num, sort_rule=str(sort_rule),
                current_page=str(current_page), min_price=str(min_price), max_price=str(max_price))    # 实例化自定义的Result_url对象


    if int(ds_name_num) <= 0 or int(ds_name_num) > 15 or int(min_price) > int(max_price) or len(baby_list) == 0:
        return render_template('get_nothing.html', price_set=price_set, search_bar=search_bar, search_baby=search_baby,
    baby_list=baby_list, search_shop=search_shop, current_page=current_page, sort_rule=sort_rule,
    min_price=min_price, max_price=max_price, all_pages=all_pages, result_url=result_url)


    return render_template('search_result.html', price_set=price_set, search_bar=search_bar, search_baby=search_baby,
    baby_list=baby_list, search_shop=search_shop, current_page=str(current_page), sort_rule=str(sort_rule),
    min_price=str(min_price), max_price=str(max_price), all_pages=str(all_pages), result_url=result_url)



