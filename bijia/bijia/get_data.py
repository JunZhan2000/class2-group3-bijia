from jieba import lcut
from gensim.similarities import SparseMatrixSimilarity
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from bijia.db import DBSession, Babies
import numpy


def babies_by_ds_name(babies, search_shop_dic):
    '''输入一个商品列表，依据需要的商城返回一个新的商品列表'''
    baby_list = []

    if search_shop_dic['taobao']:
        '''需要淘宝与天猫的数据'''
        baby_list += [baby for baby in babies if baby.ds_name == '淘宝网' or baby.name == '天猫商城']
    if search_shop_dic['jingdong']:
        '''需要京东的数据'''
        baby_list += [baby for baby in babies if baby.ds_name == '京东商城']
    if search_shop_dic['suning']:
        '''需要苏宁的数据'''
        baby_list += [baby for baby in babies if baby.ds_name == '苏宁易购']
    if search_shop_dic['dangdang']:
        '''需要当当网的数据'''
        baby_list += [baby for baby in babies if baby.ds_name == '当当网']

    return baby_list



# 获取商品的价格
def TakePrice(elem):
    return elem.price

# 获取商品的销量
def TakeSellNum(elem):
    return elem.sell_num




def get_baby_list(keyword, search_shop_dic, sort_rule, min_price, max_price):
    '''根据传入的五个参数，在数据库中检索后，返回一个有序的商品列表'''

    # 检索数据库，获得宝贝列表
    session = DBSession()
    # 价格筛选
    if min_price == -1 and max_price == 0:
        babies = session.query(Babies).filter().all()
    else:
        babies = session.query(Babies).filter((Babies.price >= min_price) & (Babies.price <= max_price)).all()
    session.close()

    # 电商筛选
    babies = babies_by_ds_name(babies=babies, search_shop_dic=search_shop_dic)

    texts = [baby.name for baby in babies]

    # 将文本集生成分词列表
    text_list = [lcut(text) for text in texts]
    # 基于文本集建立词典，并获得词典特征数
    dictionary = Dictionary(text_list)
    num_features = len(dictionary.token2id)
    # 基于词典，将分词列表集转换成稀疏向量集
    corpus = [dictionary.doc2bow(text) for text in text_list]
    # 用词典把搜索词也转换为稀疏向量
    kw_vector = dictionary.doc2bow(lcut(keyword))
    # 创建TF-IDF模型，传入语料库来训练
    tfidf = TfidfModel(corpus)
    # 用训练好的TF-IDF模型处理被检索文本和搜索词
    tf_texts = tfidf[corpus]  # 此处将【语料库】用作【被检索文本】
    tf_kw = tfidf[kw_vector]
    # 似度计算
    sparse_matrix = SparseMatrixSimilarity(tf_texts, num_features)
    similarities = sparse_matrix.get_similarities(tf_kw)
    for e, s in enumerate(similarities, 1):
        print('kw 与 text%d 相似度为：%.2f' % (e, s))
    '''获取关联度最高的前50个商品'''
    max_args = numpy.argsort(-similarities)
    baby_list = []
    for i in max_args[0: 30]:
        baby_list.append(babies[i])
        print(texts[i])

    # 依据排序规则对商品进行排序
    if sort_rule == 1:
        # 综合排序
        baby_list.sort(key=TakePrice, reverse=False)
    elif sort_rule == 2:
        '''价格升序'''
        baby_list.sort(key=TakePrice, reverse=False)
    elif sort_rule == 3:
        '''价格降序'''
        baby_list.sort(key=TakePrice, reverse=True)
    elif sort_rule == 4:
        '''销量排序'''
        baby_list.sort(key=TakeSellNum, reverse=True)


    return baby_list
