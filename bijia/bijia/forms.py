from flask_wtf import FlaskForm
from wtforms import Form, StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class Search_bar(FlaskForm):
    '''搜索栏表单，用于读取用户想查找的商品名'''
    baby = StringField(label=u'baby', validators=[DataRequired(message=u'商品名不能为空!　ﾟヽ(ﾟ´Д`)ﾉﾟ')])
    submit = SubmitField(label=u'全文搜索')

    all = BooleanField(label=u'全网搜索')
    taobao = BooleanField(label=u'淘宝')
    jingdong = BooleanField(label=u'京东')
    suning = BooleanField(label=u'苏宁易购')
    dangdang = BooleanField(label=u'当当')



class Price_set(FlaskForm):
    '''价格区间表单，用于筛选商品'''
    min_price = StringField(label=u'最低价格', validators=[DataRequired()])
    max_price = StringField(label=u'最高价格', validators=[DataRequired()])

    price_submit = SubmitField(label=u'确认')
