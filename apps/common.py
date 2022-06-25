# -*- coding: utf-8 -*-
# @Time    : 2022/6/25 16:40
# @Author  : 十一
# @Email   : 981742876.com
# @File    : db_common.py
# @Desc    : 公共模块
from urllib.parse import urlencode

from flask import Blueprint, request

from extend import mail, db
from flask_mail import Message
import string
import random
import requests
from datetime import datetime
from models.db_common import EmailCodeModel, PhoneCodeModel

common = Blueprint('common', __name__, url_prefix='/common')


# 发送手机验证码
@common.route('/send_phone_code', methods=["GET"])
def send_phone_code():
    phone = request.args.get('phone')
    print(phone)
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
            return "数据已存在"
        else:
            phone_models = PhoneCodeModel(code=code, phone=phone)
            db.session.add(phone_models)
            db.session.commit()
            return "插入成功"
    else:
        return "发送失败"


# 发送邮箱验证码
@common.route('/send_code', methods=['GET'])
def send_code():
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


# 登录
@common.route('/login')
def login():
    return "登录"


# 注册
@common.route('/register')
def register():
    pass
