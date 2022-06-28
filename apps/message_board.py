#!/usr/bin/env python3
"""
@Author   ：十一
@Email    ：981742876@qq.com
@Time     ：2022/6/28 11:49
@Desc     : 留言板
"""
from flask import Blueprint, jsonify, request, g
from extend import db
import os
from decorators import login_state, is_admin
from flasgger import swag_from
from models.db_message_board import MessageBoardModel
from models.db_common import UserModel

message_board = Blueprint('message_board', __name__, url_prefix='/message_board')


# 获取留言列表
@message_board.route('/get_message_board')
@login_state
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/message_board/get_message_board.yaml")
def get_message_board():
    page = request.args.get('current')
    page_size = request.args.get('pageSize')
    paginates = MessageBoardModel.query.filter_by(parent_id=None).paginate(page=int(page), per_page=int(page_size))
    has_next = paginates.has_next  # 是否有下一页
    has_prev = paginates.has_prev  # 是否有上一页
    total = paginates.total  # 总条数
    resources_list = []
    for item in paginates.items:
        items = item.to_json()
        items['create_time'] = str(items['create_time'])
        items['update_time'] = str(items['update_time'])
        user = UserModel.query.filter_by(id=items['user_id']).first()
        items['user_name'] = user.user_name
        items['avatar_url'] = user.avatar_url
        items['child'] = []
        children_model = MessageBoardModel.query.filter_by(parent_id=items['id']).all()
        for child in children_model:
            childs = child.to_json()
            comment_user = UserModel.query.filter_by(id=childs['user_id']).first()
            childs['user_name'] = comment_user.user_name
            childs['avatar_url'] = comment_user.avatar_url
            childs['create_time'] = str(childs['create_time'])
            childs['update_time'] = str(childs['update_time'])
            items['child'].append(childs)

        resources_list.append(items)
    return jsonify({"message": "操作成功",
                    "data": {"data": resources_list, "total": total, "has_next": has_next, "has_prev": has_prev},
                    'code': 200})


# 新增留言
@message_board.route('/add_message_board', methods=["POST"])
@login_state
@is_admin
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/message_board/add_message_board.yaml")
def add_message_board():
    resources_classify = MessageBoardModel(title=request.get_json()['title'],
                                           content=request.get_json()['content'],
                                           user_id=g.user.id)
    db.session.add(resources_classify)
    db.session.commit()
    return jsonify({"message": "操作成功", "data": None, 'code': 200})


# 评论留言
@message_board.route('/comment_message_board', methods=["POST"])
@login_state
@is_admin
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/message_board/comment_message_board.yaml")
def comment_message_board():
    resources_classify = MessageBoardModel(
        content=request.get_json()['content'],
        parent_id=request.get_json()['parent_id'],
        user_id=g.user.id,
    )
    db.session.add(resources_classify)
    db.session.commit()
    return jsonify({"message": "操作成功", "data": None, 'code': 200})


# 删除留言
@message_board.route('/delete_message_board', methods=["DELETE"])
@login_state
@is_admin
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/message_board/delete_message_board.yaml")
def delete_message_board():
    try:
        resources_classify = MessageBoardModel.query.filter_by(id=request.args.get('id')).first()
        db.session.delete(resources_classify)
        db.session.commit()
        return jsonify({"message": "操作成功", "data": None, 'code': 200})
    except:
        return jsonify({"message": "没有该数据", "data": None, 'code': 1001})
