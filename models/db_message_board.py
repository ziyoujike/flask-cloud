#!/usr/bin/env python3
"""
@Author   ：十一
@Email    ：981742876@qq.com
@Time     ：2022/6/28 11:52
@Desc     : 
@File    : db_message_board.py
"""

from extend import db
from datetime import datetime

import uuid


# 留言板
class MessageBoardModel(db.Model):
    __tablename__ = 'db_message_board'
    id = db.Column(db.String(64), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(db.String(64), db.ForeignKey('db_user.id'))
    user = db.relationship("UserModel", backref="db_message_board")
    parent_id = db.Column(db.String(64), default=None)
    title = db.Column(db.Text(), default=None)
    content = db.Column(db.Text())
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now)

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item
