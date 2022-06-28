# -*- coding: utf-8 -*-
# @Time    : 2022/6/25 16:40
# @Author  : 十一
# @Email   : 981742876.com
# @File    : db_common.py
# @Desc    : 公共模块
import json
import os
from urllib.parse import urlencode

from flask import Blueprint, request, jsonify, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from extend import mail, db
from flask_mail import Message
import string
import random
import requests
from qiniu import Auth
from datetime import datetime
from models.db_common import EmailCodeModel, PhoneCodeModel, UserModel, DictionariesModel

from flasgger import swag_from
from decorators import login_state, is_admin

common = Blueprint('common', __name__, url_prefix='/common')

# 七牛给开发者分配的AccessKey
QINIU_ACCESS_KEY = 'NwAngZAu-NMd1hnONYBKVLlZIrTl7XvW1003FceC'
# 七牛给开发者分配的Secret
QINIU_SECRET_KEY = '0Z80IWpG3UcvHKj9lMedQi83rfV9GKT6WfxvNE1t'


# 发送手机验证码
@common.route('/send_phone_code', methods=["GET"])
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/common/send_phone_code.yaml")
def send_phone_code():
    phone = request.args.get('phone')
    url = "http://v.juhe.cn/sms/send"
    code = '%06d' % random.randint(0, 999999)
    params = {
        "mobile": phone,  # 接受短信的用户手机号码
        "tpl_id": "245380",  # 您申请的短信模板ID，根据实际情况修改
        "tpl_value": "#code#={}".format(code),  # 您设置的模板变量，根据实际情况修改
        "key": "6898c9eb0ed8ff65bd83180ac32dee06",  # 应用KEY(应用详细页查询)
    }
    params = urlencode(params)
    r = requests.get(url, params)
    if r.status_code == 200:
        phone_model = PhoneCodeModel.query.filter_by(phone=phone).first()
        if phone_model:
            phone_model.code = code
            phone_model.update_time = datetime.now()
            db.session.commit()
            return jsonify({"message": "操作成功", "data": None, 'code': 200})
        else:
            phone_models = PhoneCodeModel(code=code, phone=phone)
            db.session.add(phone_models)
            db.session.commit()
            return jsonify({"message": "操作成功", "data": None, 'code': 200})

    else:
        return jsonify({"message": "服务器错误", "data": None, 'code': 1001})


# 发送邮箱验证码
@common.route('/send_email_code', methods=['GET'])
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/common/send_email_code.yaml")
def send_email_code():
    email = request.args.get('email')
    letters = string.ascii_letters + string.digits
    code = "".join(random.sample(letters, 4))
    if email:
        message = Message(
            subject="Cloud 邮箱验证",
            recipients=[email],
            body="您的验证码为 【{}】,如非本人操作，请忽略！".format(code)
        )
        mail.send(message)
        email_model = EmailCodeModel.query.filter_by(email=email).first()
        if email_model:
            email_model.code = code
            email_model.update_time = datetime.now()
            db.session.commit()
            return jsonify({"message": "操作成功", "data": None, 'code': 200})
        else:
            email_models = EmailCodeModel(email=email, code=code)
            db.session.add(email_models)
            db.session.commit()
            return jsonify({"message": "操作成功", "data": None, 'code': 200})
    else:
        return jsonify({"message": "没有传递邮箱", "data": None, 'code': 1001})


# 七牛上传文件获取token
@common.route('/upload_file', methods=['GET'])
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/common/upload_file.yaml")
def upload_file():
    q = Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)
    # 要上传的空间
    bucket_name = 'geek-img-space'
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, expires=3600)
    return jsonify({"message": "操作成功", "data": token, 'code': 1001})


# 注册
@common.route('/register', methods=['POST'])
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/common/register.yaml")
def register():
    user_model = UserModel.query.filter_by(phone=request.get_json()['phone']).first()
    phone_model = PhoneCodeModel.query.filter_by(phone=request.get_json()['phone']).first()
    if phone_model:
        if phone_model.code == request.get_json()['phone_code']:
            if user_model:
                print()
                return jsonify({"message": "该用户已存在", "data": None, 'code': 1001})
            else:
                # 密码加密
                hash_password = generate_password_hash("123456")
                user_models = UserModel(
                    phone=request.get_json()['phone'],
                    password=hash_password
                )
                db.session.add(user_models)
                db.session.commit()
                return jsonify({"message": "注册成功", "data": None, 'code': 200})
        else:
            return jsonify({"message": "验证码错误", "data": None, 'code': 1001})
    else:
        return jsonify({"message": "验证码错误", "data": None, 'code': 1001})


# 登录
@common.route('/login', methods=["POST"])
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/common/login.yaml")
def login():
    user_model = UserModel.query.filter_by(phone=request.get_json()['phone']).first()
    phone_model = PhoneCodeModel.query.filter_by(phone=request.get_json()['phone']).first()
    if user_model:
        if user_model and (
                phone_model.code == request.get_json()['phone_code'] or check_password_hash(user_model.password,
                                                                                            request.get_json()[
                                                                                                'password'])):
            session['user_id'] = user_model.id
            return jsonify({"message": "登录成功", "data": None, 'code': 200})
        else:
            return jsonify({"message": "账号或密码错误", "data": None, 'code': 1001})
    else:
        return jsonify({"message": "账号不存在", "data": None, 'code': 1001})


# 退出登录
@common.route('/login_out')
@login_state
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/common/login_out.yaml")
def login_out():
    session.clear()
    return jsonify({"message": "操作成功", "data": None, 'code': 200})


# 修改用户信息
@common.route('/update_user_info', methods=['POST'])
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/common/update_user_info.yaml")
def update_user_info():
    user_model = UserModel.query.filter_by(id=g.user.id).first()
    user_model.avatar_url = request.get_json()['avatar_url']
    user_model.email = request.get_json()['email']
    user_model.user_name = request.get_json()['user_name']
    db.session.commit()
    return jsonify({"message": "操作成功", "data": None, 'code': 200})


# 修改密码
@common.route('/update_password', methods=['POST'])
@login_state
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/common/update_password.yaml")
def update_password():
    try:
        user_model = UserModel.query.filter_by(id=g.user.id).first()
        phone_model = PhoneCodeModel.query.filter_by(phone=request.get_json()['phone']).first()
        if phone_model.code == request.get_json()['phone_code']:
            user_model.password = generate_password_hash(request.get_json()['password'])
            db.session.commit()
            return jsonify({"message": "操作成功", "data": None, 'code': 200})
        else:
            return jsonify({"message": "验证码错误,请重新输入", "data": None, 'code': 200})
    except:
        pass


# 获取用户信息
@common.route('/get_user_info')
@login_state
@is_admin
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/common/get_user_info.yaml")
def get_user_info():
    user_info = {
        "id": g.user.id,
        "user_name": g.user.user_name,
        "phone": g.user.phone,
        "avatar_url": g.user.avatar_url,
        "email": g.user.email,
    }
    return jsonify({"message": "获取用户信息成功", "data": user_info, 'code': 200})


# 获取用户列表
@common.route('/get_user_list')
@login_state
@is_admin
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/common/get_user_list.yaml")
def get_user_list():
    page = request.args.get('current')
    page_size = request.args.get('pageSize')
    paginates = UserModel.query.paginate(page=int(page), per_page=int(page_size))
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


# 获取字典列表
@common.route('/get_dictionaries_list')
@login_state
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/common/get_dictionaries_list.yaml")
def get_dictionaries_list():
    page = request.args.get('current')
    page_size = request.args.get('pageSize')
    paginates = DictionariesModel.query.paginate(page=int(page), per_page=int(page_size))
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


# 新增字典
@common.route('/add_dictionaries', methods=["POST"])
@login_state
@is_admin
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/common/add_dictionaries.yaml")
def add_dictionaries():
    try:
        resources_classify = DictionariesModel(title=request.get_json()['title'],
                                               type=request.get_json()['type'],
                                               code=request.get_json()['code'],
                                               icon_url=request.get_json()['icon_url'],
                                               user_id=g.user.id)
        db.session.add(resources_classify)
        db.session.commit()
        return jsonify({"message": "操作成功", "data": None, 'code': 200})
    except:
        pass


# 删除字典
@common.route('/delete_dictionaries', methods=["DELETE"])
@login_state
@is_admin
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/common/delete_dictionaries.yaml")
def delete_dictionaries():
    try:
        resources_classify = DictionariesModel.query.filter_by(id=request.args.get('id')).first()
        db.session.delete(resources_classify)
        db.session.commit()
        return jsonify({"message": "操作成功", "data": None, 'code': 200})
    except:
        return jsonify({"message": "没有该数据", "data": None, 'code': 1001})


# 修改字典
@common.route('/update_dictionaries', methods=["PUT"])
@login_state
@is_admin
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/common/update_dictionaries.yaml")
def update_dictionaries():
    try:
        resources_model = DictionariesModel.query.filter_by(id=request.get_json()['id']).first()
        resources_model.title = request.get_json()['title']
        resources_model.type = request.get_json()['type']
        resources_model.code = request.get_json()['code']
        resources_model.icon_url = request.get_json()['icon_url']
        resources_model.user_id = g.user.id
        db.session.commit()

        return jsonify({"message": "操作成功", "data": None, 'code': 200})
    except:
        return jsonify({"message": "参数错误", "data": None, 'code': 200})
