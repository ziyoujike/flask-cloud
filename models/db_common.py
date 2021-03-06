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

import uuid


# 用户
class UserModel(db.Model):
    __tablename__ = 'db_user'
    id = db.Column(db.String(64), primary_key=True, default=uuid.uuid4)
    user_name = db.Column(db.String(255))
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False, unique=True)
    avatar_url = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=False)
    user_type = db.Column(db.Integer, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now)
    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


# 字典
class DictionariesModel(db.Model):
    __tablename__ = 'db_dictionaries'
    id = db.Column(db.String(64), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(20))
    type = db.Column(db.String(20))
    code = db.Column(db.Integer)
    icon_url = db.Column(db.String(255))
    user_id = db.Column(db.String(64), db.ForeignKey('db_user.id'))
    user = db.relationship("UserModel", backref="db_dictionaries")
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now)
    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item

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
