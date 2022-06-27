# -*- coding: utf-8 -*-
# @Time    : 2022/6/25 16:51
# @Author  : 十一
# @Email   : 981742876.com
# @File    : resources.py
# @Desc    : 资源模块

from flask import Blueprint, jsonify
import os
from decorators import login_state, is_admin
from flasgger import swag_from

from models.db_resources import ResourcesClassifyModel

resources = Blueprint('resources', __name__, url_prefix='/resources')


# 获取资源分类列表
@resources.route('/get_resources_classify')
@login_state
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/resources/get_resources_classify.yaml")
def get_resources_classify():
    resources_model = ResourcesClassifyModel.query.all()
    print(resources_model)
    return jsonify({"message": "操作成功", "data": None, 'code': 200})


# 新增资源分类
@resources.route('/add_resources_classify', methods=["POST"])
@login_state
@is_admin
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/resources/add_resources_classify.yaml")
def add_resources_classify():
    resources_model = ResourcesClassifyModel.query.all()
    print(resources_model)
    return jsonify({"message": "操作成功", "data": None, 'code': 200})


# 删除资源分类
@resources.route('/delete_resources_classify', methods=["DELETE"])
@login_state
@is_admin
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/resources/delete_resources_classify.yaml")
def delete_resources_classify():
    resources_model = ResourcesClassifyModel.query.all()
    print(resources_model)
    return jsonify({"message": "操作成功", "data": None, 'code': 200})


# 修改资源分类
@resources.route('/update_resources_classify', methods=["PUT"])
@login_state
@is_admin
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/resources/update_resources_classify.yaml")
def update_resources_classify():
    resources_model = ResourcesClassifyModel.query.all()
    print(resources_model)
    return jsonify({"message": "操作成功", "data": None, 'code': 200})


# 获取资源分类列表
@resources.route('/get_resources')
@login_state
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/resources/get_resources.yaml")
def get_resources():
    resources_model = ResourcesClassifyModel.query.all()
    print(resources_model)
    return jsonify({"message": "操作成功", "data": None, 'code': 200})


# 新增资源分类
@resources.route('/add_resources', methods=["POST"])
@login_state
@is_admin
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/resources/add_resources.yaml")
def add_resources():
    resources_model = ResourcesClassifyModel.query.all()
    print(resources_model)
    return jsonify({"message": "操作成功", "data": None, 'code': 200})


# 删除资源分类
@resources.route('/delete_resources', methods=["DELETE"])
@login_state
@is_admin
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/resources/delete_resources.yaml")
def delete_resources():
    resources_model = ResourcesClassifyModel.query.all()
    print(resources_model)
    return jsonify({"message": "操作成功", "data": None, 'code': 200})


# 修改资源分类
@resources.route('/update_resources', methods=["PUT"])
@login_state
@is_admin
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/resources/update_resources.yaml")
def update_resources():
    resources_model = ResourcesClassifyModel.query.all()
    print(resources_model)
    return jsonify({"message": "操作成功", "data": None, 'code': 200})
