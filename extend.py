# -*- coding: utf-8 -*-
# @Time    : 2022/6/25 14:56
# @Author  : 十一
# @Email   : 981742876.com
# @File    : extend.py
# @Desc    : 扩展

from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()

mail = Mail()
