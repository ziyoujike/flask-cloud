# -*- coding: utf-8 -*-
# @Time    : 2022/6/25 16:51
# @Author  : 十一
# @Email   : 981742876.com
# @File    : resources.py
# @Desc    : 资源模块

from flask import Blueprint

resources = Blueprint('resources', __name__, url_prefix='/resources')


@resources.route('/get_resources')
def get_resources():
    return "获取资源列表"
