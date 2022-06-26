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

from datetime import datetime
from models.db_common import EmailCodeModel, PhoneCodeModel, UserModel

from flasgger import swag_from

common = Blueprint('common', __name__, url_prefix='/common')


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
            return jsonify({"message": "数据已存在", "code": 1001})
        else:
            phone_models = PhoneCodeModel(code=code, phone=phone)
            db.session.add(phone_models)
            db.session.commit()
            return jsonify({"message": "发送成功", "code": 200})
    else:
        return jsonify({"message": "服务器错误", "code": 1002})


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
            return "数据已存在"
        else:
            email_models = EmailCodeModel(email=email, code=code)
            db.session.add(email_models)
            db.session.commit()
            return "插入成功"
    else:
        return "没有传递邮箱"


# 注册
@common.route('/register', methods=['POST'])
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/common/register.yaml")
def register():
    user_model = UserModel.query.filter_by(phone=request.get_json()['phone']).first()
    if user_model:
        print()
        return jsonify({"message": "该用户已存在", "data": None, 'code': 1001})
    else:
        # 密码加密
        hash_password = generate_password_hash(request.get_json()['password'])
        user_models = UserModel(
            phone=request.get_json()['phone'],
            email=request.get_json()['email'],
            password=hash_password
        )
        db.session.add(user_models)
        db.session.commit()
        print(generate_password_hash(request.get_json()['password']))
        return jsonify({"message": "注册成功", "data": None, 'code': 200})


# 登录
@common.route('/login', methods=["POST"])
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/common/login.yaml")
def login():
    user_model = UserModel.query.filter_by(phone=request.get_json()['phone']).first()
    if user_model:
        password = request.get_json()['password']
        if user_model and check_password_hash(user_model.password, password):
            session['user_id'] = user_model.id
            return jsonify({"message": "登录成功"})
        else:
            return jsonify({"message": "账号或密码错误"})
    else:
        return jsonify({"message": "账号不存在"})


# 登录
@common.route('/login_out')
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/common/login_out.yaml")
def login_out():
    session.clear()
    return jsonify({"message": "操作成功", "data": None, 'code': 200})


# 修改用户信息
@common.route('/update_user_info', methods=['POST'])
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/common/update_user_info.yaml")
def update_user_info():
    if hasattr(g, 'user'):
        print(g.user.id)
    return jsonify({"message": "OK", "data": None, 'code': 1003})


# 获取用户信息
@common.route('/get_user_info')
@swag_from(os.path.abspath('..') + "/flask-cloud/apidocs/common/get_user_info.yaml")
def get_user_info():
    if hasattr(g, 'user'):
        print(g.user.id)
        user_info = {
            "id": g.user.id,
            "user_name": g.user.user_name,
            "phone": g.user.phone,
            "avatar_url": g.user.avatar_url,
            "email": g.user.email,
        }
        return jsonify({"message": "获取用户信息成功", "data": user_info, 'code': 200})
    else:
        return jsonify({"message": "用户不存在", "data": None, 'code': 1003})
