babies.xls 是从数据库导出的商品表
（手机商品，约有一万四千条记录）




search_baby是用于爬取数据并更新数据库的项目
需要安装的库有requests, lxml, bs4, SQLAlchemy, mysql-connector-python




bijia是用于运行网站的项目
需要安装的库有Flask, wtforms, Flask-wtf, SQLAlchemy, mysql-connector-python, jieba, genism

运行该项目需依次输入命令：
set FLASK_APP=bijia
flask run