# -*- coding: utf-8 -*-
# @Time    : 2022/6/25 14:31
# @Author  : 十一
# @Email   : 981742876.com
# @File    : db_common.py
# @Desc    : 公共模块

"""
unique 只能存在一份
autoincrement 自增长
nullable 不能为空
"""

from extend import db
from datetime import datetime

# 表单验证
import wtforms
import uuid


# 用户
class UserModel(db.Model):
    __tablename__ = 'db_user'
    id = db.Column(db.String(64), primary_key=True, default=uuid.uuid4)
    user_name = db.Column(db.String(255))
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False, unique=True)
    avatar_url = db.Column(db.String(255))
    email = db.Column(db.String(255))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now)


# 字典
class DictionariesModel(db.Model):
    __tablename__ = 'db_dictionaries'
    id = db.Column(db.String(64), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(20))
    type = db.Column(db.String(20))
    code = db.Column(db.String(4))
    icon_url = db.Column(db.String(255))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now)


# 手机验证码

class PhoneCodeModel(db.Model):
    __tablename__ = 'db_phone_code'
    id = db.Column(db.String(64), primary_key=True, default=uuid.uuid4)
    phone = db.Column(db.String(255), nullable=False, unique=True)
    code = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now)


# 邮箱验证码

class EmailCodeModel(db.Model):
    __tablename__ = 'db_email_code'
    id = db.Column(db.String(64), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(255), nullable=False, unique=True)
    code = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now)
