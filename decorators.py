#!/usr/bin/env python3
"""
@Author   ：十一
@Email    ：981742876@qq.com
@Time     ：2022/6/27 12:03
@Desc     : 装饰器
"""

from flask import g, jsonify
from functools import wraps


def login_state(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if hasattr(g, 'user'):
            return func(*args, **kwargs)
        else:
            return jsonify({"message": "用户不存在", "data": None, 'code': 1001})

    return wrapper


def is_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        if g.user.user_type == 1:
            return func(*args, **kwargs)
        else:
            return jsonify({"message": "暂无权限", "data": None, 'code': 1001})

    return wrapper
