def zip_search_shop(all, taobao, jingdong, suning, dangdang):
    '''判定在哪些商城爬取数据'''
    search_shop = 15
    if all == False:
        '''如果没有勾选全网搜索，则判定勾选了哪些其他选项'''
        if taobao == True:
            if_taobao = 1
        else:
            if_taobao = 0

        if jingdong == True:
            if_jingdong = 1
        else:
            if_jingdong = 0

        if suning == True:
            if_suning = 1
        else:
            if_suning = 0
        if dangdang == True:
            if_dangdang = 1
        else:
            if_dangdang = 0
        search_shop = 8 * if_taobao + 4 * if_jingdong + 2 * if_suning + 1 * if_dangdang
    return search_shop


def get_search_shop(search_shop):
    search_shop_dic = {
        'taobao': True,
        'jingdong': True,
        'suning': True,
        'dangdang': True
    }
    if search_shop == 14:
        search_shop_dic['dangdang'] = False
    if search_shop == 13:
        search_shop_dic['suning'] = False
    if search_shop == 12:
        search_shop_dic['dangdang'] = False
        search_shop_dic['suning'] = False
    if search_shop == 11:
        search_shop_dic['jingdong'] = False
    if search_shop == 10:
        search_shop_dic['jingdong'] = False
        search_shop_dic['dangdang'] = False
    if search_shop == 9:
        search_shop_dic['jingdong'] = False
        search_shop_dic['suning'] = False
    if search_shop == 8:
        search_shop_dic['jingdong'] = False
        search_shop_dic['suning'] = False
        search_shop_dic['dangdang'] = False
    if search_shop == 7:
        search_shop_dic['taobao'] = False
    if search_shop == 6:
        search_shop_dic['taobao'] = False
        search_shop_dic['dangdang'] = False
    if search_shop == 5:
        search_shop_dic['taobao'] = False
        search_shop_dic['suning'] = False
    if search_shop == 4:
        search_shop_dic['taobao'] = False
        search_shop_dic['suning'] = False
        search_shop_dic['dangdang'] = False
    if search_shop == 3:
        search_shop_dic['taobao'] = False
        search_shop_dic['jingdong'] = False
    if search_shop == 2:
        search_shop_dic['taobao'] = False
        search_shop_dic['jingdong'] = False
        search_shop_dic['dangdang'] = False
    if search_shop == 1:
        search_shop_dic['taobao'] = False
        search_shop_dic['jingdong'] = False
        search_shop_dic['suning'] = False
    if search_shop == 0:
        search_shop_dic['taobao'] = False
        search_shop_dic['jingdong'] = False
        search_shop_dic['suning'] = False
        search_shop_dic['dangdang'] = False

    return search_shop_dic


class Result_url(object):
    '''用于对搜索结果页面的url进行修改的对象'''
    def __init__(self, search_baby, ds_name_num, sort_rule, current_page, min_price, max_price):
        # 拼接起来即为网址饿肚肚字符串列表，分别为前缀加商品名加电商名，排序规则，斜杠，当前页码， 最低价加最高价五个元素
        self.url = ['http://127.0.0.1:5000/search_result/' + search_baby + '/' + ds_name_num + '/',
                    sort_rule, '/' , current_page, '/' + min_price + '/' + max_price + '']

    def get_url(self):
        return self.url[0] + self.url[1] + self.url[2] + self.url[3] + self.url[4]

    def change_sort_rule(self, new_sort_rule):
        '''使用新的排序规则，并返回替换后的网址,不改变原有属性'''
        # self.url[1] = new_sort_rule    # 用新的排序规则替换原有的
        return self.url[0] + new_sort_rule + self.url[2] + self.url[3] + self.url[4]    # 返回新页码的拼接网址


    def change_page(self, new_page):
        # 使用新的页码
        # self.url[3] = new_page    # 用新的页码替换原有的
        return self.url[0] + self.url[1] + self.url[2] + new_page + self.url[4]    # 返回新页码的拼接网址


















