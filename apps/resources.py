# -*- coding: utf-8 -*-
# @Time    : 2022/6/25 16:51
# @Author  : 十一
# @Email   : 981742876.com
# @File    : resources.py
# @Desc    : 资源模块

from flask import Blueprint, jsonify, request, g
from extend import db
import os
from decorators import login_state, is_admin
from flasgger import swag_from
from models.db_resources import ResourcesClassifyModel, ResourcesModel

resources = Blueprint('resources', __name__, url_prefix='/resources')


# 获取资源分类列表
@resources.route('/get_resources_classify')
@login_state
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/resources/get_resources_classify.yaml")
def get_resources_classify():
    page = request.args.get('current')
    page_size = request.args.get('pageSize')
    paginates = ResourcesClassifyModel.query.paginate(page=int(page), per_page=int(page_size))
    has_next = paginates.has_next  # 是否有下一页
    has_prev = paginates.has_prev  # 是否有上一页
    total = paginates.total  # 总条数
    resources_list = []
    for item in paginates.items:
        items = item.to_json()
        items['create_time'] = str(items['create_time'])
        items['update_time'] = str(items['update_time'])
        resources_list.append(items)
    return jsonify({"message": "操作成功",
                    "data": {"data": resources_list, "total": total, "has_next": has_next, "has_prev": has_prev},
                    'code': 200})


# 新增资源分类
@resources.route('/add_resources_classify', methods=["POST"])
@login_state
@is_admin
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/resources/add_resources_classify.yaml")
def add_resources_classify():
    resources_classify = ResourcesClassifyModel(title=request.get_json()['title'],
                                                img_url=request.get_json()['img_url'], desc=request.get_json()['desc'],
                                                user_id=g.user.id)
    db.session.add(resources_classify)
    db.session.commit()
    return jsonify({"message": "操作成功", "data": None, 'code': 200})


# 删除资源分类
@resources.route('/delete_resources_classify', methods=["DELETE"])
@login_state
@is_admin
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/resources/delete_resources_classify.yaml")
def delete_resources_classify():
    try:
        resources_classify = ResourcesClassifyModel.query.filter_by(id=request.args.get('id')).first()
        db.session.delete(resources_classify)
        db.session.commit()
        return jsonify({"message": "操作成功", "data": None, 'code': 200})
    except:
        return jsonify({"message": "没有该数据", "data": None, 'code': 1001})


# 修改资源分类
@resources.route('/update_resources_classify', methods=["PUT"])
@login_state
@is_admin
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/resources/update_resources_classify.yaml")
def update_resources_classify():
    try:
        resources_model = ResourcesClassifyModel.query.filter_by(id=request.get_json()['id']).first()
        resources_model.title = request.get_json()['title']
        resources_model.img_url = request.get_json()['img_url']
        resources_model.desc = request.get_json()['desc']
        resources_model.user_id = g.user.id
        db.session.commit()

        return jsonify({"message": "操作成功", "data": None, 'code': 200})
    except:
        return jsonify({"message": "参数错误", "data": None, 'code': 200})


# 获取资源列表
@resources.route('/get_resources')
@login_state
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/resources/get_resources.yaml")
def get_resources():
    page = request.args.get('current')
    page_size = request.args.get('pageSize')
    paginates = ResourcesModel.query.paginate(page=int(page), per_page=int(page_size))
    has_next = paginates.has_next  # 是否有下一页
    has_prev = paginates.has_prev  # 是否有上一页
    total = paginates.total  # 总条数
    resources_list = []
    for item in paginates.items:
        items = item.to_json()
        items['create_time'] = str(items['create_time'])
        items['update_time'] = str(items['update_time'])
        resources_list.append(items)
    return jsonify({"message": "操作成功",
                    "data": {"data": resources_list, "total": total, "has_next": has_next, "has_prev": has_prev},
                    'code': 200})
    # resources_model = ResourcesModel.query.all()
    # resources_list = []
    # for item in resources_model:
    #     # 通过遍历结果集 我们将每一条记录转化为json
    #     items = item.to_json()
    #     resources_classify_model = ResourcesClassifyModel.query.filter_by(id=items['resources_classify_id']).first()
    #
    #     items['resources_classify_title'] = resources_classify_model.title
    #     items['create_time'] = str(items['create_time'])
    #     items['update_time'] = str(items['update_time'])
    #     resources_list.append(items)
    # return jsonify({"message": "操作成功", "data": resources_list, 'code': 200})


# 新增资源
@resources.route('/add_resources', methods=["POST"])
@login_state
@is_admin
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/resources/add_resources.yaml")
def add_resources():
    try:
        resources_model = ResourcesModel(title=request.get_json()['title'],
                                         img_url=request.get_json()['img_url'],
                                         desc=request.get_json()['desc'],
                                         link=request.get_json()['link'],
                                         resources_classify_id=request.get_json()['resources_classify_id'],
                                         sort=request.get_json()['sort'],
                                         user_id=g.user.id
                                         )
        db.session.add(resources_model)
        db.session.commit()
        return jsonify({"message": "操作成功", "data": None, 'code': 200})

    except:
        return jsonify({"message": "参数错误", "data": None, 'code': 200})


# 删除资源
@resources.route('/delete_resources', methods=["DELETE"])
@login_state
@is_admin
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/resources/delete_resources.yaml")
def delete_resources():
    try:
        resources_model = ResourcesModel.query.filter_by(id=request.args.get('id')).first()
        db.session.delete(resources_model)
        db.session.commit()
        return jsonify({"message": "操作成功", "data": None, 'code': 200})
    except:
        return jsonify({"message": "没有该数据", "data": None, 'code': 1001})


# 修改资源
@resources.route('/update_resources', methods=["PUT"])
@login_state
@is_admin
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/resources/update_resources.yaml")
def update_resources():
    try:
        resources_model = ResourcesModel.query.filter_by(id=request.get_json()['id']).first()
        resources_model.title = request.get_json()['title']
        resources_model.img_url = request.get_json()['img_url']
        resources_model.desc = request.get_json()['desc']
        resources_model.link = request.get_json()['link']
        resources_model.resources_classify_id = request.get_json()['resources_classify_id']
        resources_model.sort = request.get_json()['sort']
        resources_model.user_id = g.user.id
        db.session.commit()

        return jsonify({"message": "操作成功", "data": None, 'code': 200})
    except:
        return jsonify({"message": "参数错误", "data": None, 'code': 200})
