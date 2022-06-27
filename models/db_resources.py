#!/usr/bin/env python3
"""
@Author   ：十一
@Email    ：981742876@qq.com
@Time     ：2022/6/27 12:32
@Desc     : 资源model
"""

from extend import db
from datetime import datetime

import uuid


# 资源分类
class ResourcesClassifyModel(db.Model):
    __tablename__ = 'db_resources_classify'
    id = db.Column(db.String(64), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(255))
    desc = db.Column(db.String(255))
    img_url = db.Column(db.String(255))
    user_id = db.Column(db.String(64), db.ForeignKey('db_user.id'))
    user = db.relationship("UserModel", backref="db_resources_classify")
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now)





# 资源
class ResourcesModel(db.Model):
    __tablename__ = 'db_resources'
    id = db.Column(db.String(64), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(255))
    resources_classify_id = db.Column(db.String(64), db.ForeignKey('db_resources_classify.id'))
    resources_classify = db.relationship("ResourcesClassifyModel", backref="db_resources")
    link = db.Column(db.String(255))
    desc = db.Column(db.String(255))
    img_url = db.Column(db.String(255))
    is_show = db.Column(db.Integer, default=1)
    sort = db.Column(db.Integer, default=0)
    user_id = db.Column(db.String(64), db.ForeignKey('db_user.id'))
    user = db.relationship("UserModel", backref="db_resources")
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now)
