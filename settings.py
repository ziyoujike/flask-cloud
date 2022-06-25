# -*- coding: utf-8 -*-
# @Time    : 2022/6/24 19:53
# @Author  : 十一
# @Email   : 981742876.com
# @File    : settings.py
# @Desc    : 配置文件


# 解决返回JSON中文乱码问题
JSON_AS_ASCII = False

# 数据库的配置变量
HOSTNAME = 'rm-uf6w8th6if60vb548uo.mysql.rds.aliyuncs.com'
PORT = '3306'
DATABASE = 'cloud-pro'
USERNAME = 'pxtk'
PASSWORD = 'eer#$89000rtynp'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
# 是否每次跟踪修改
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = '8854ca1c-5cfd-431e-9cd7-54fe2b71c9e1'

# 邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEBUG = False
MAIL_USERNAME = "www.981742876@qq.com"
MAIL_PASSWORD = "ehpsiauvcquibefi"
MAIL_DEFAULT_SENDER = "www.981742876@qq.com"
