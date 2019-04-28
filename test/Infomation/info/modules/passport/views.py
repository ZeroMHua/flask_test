import json
import random
import re

from flask import abort, jsonify
from flask import current_app
from flask import request
from flask import session

from info import constants, db
from info.models import User
from info.utils.commons import login_required
from info.utils.response_code import RET
from . import passport_blu

from flask import make_response

from info import redis_store
from info.utils.captcha.captcha import captcha
from info.libs.yuntongxun.sms import CCP


@passport_blu.route('/logout', methods=['POST'])
def logout():
    """
    退出登录:
    1. 清除session中用户的登录状态数据
    2. 返回应答，退出成功
    """ 
    # 1. 清除session中用户的登录状态数据
    session.pop('user_id')
    session.pop('mobile')
    session.pop('nick_name')
    
    # 2. 返回应答，退出成功
    return jsonify(errno=RET.OK, errmsg='退出登录成功')
    

@passport_blu.route('/login', methods=['POST'])
def login():
    """
    用户登录:
    1. 接收参数(手机号，密码)并进行参数校验
    2. 根据`手机号`查询User信息(如果查不到，说明用户不存在)
    3. 校验用户的`密码`是否正确
    4. 记住用户的登录状态
    5. 返回应答，登录成功
    """
    # 1. 接收参数(手机号，密码)并进行参数校验
    req_dict = request.json

    if not req_dict:
        return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')

    mobile = req_dict.get('mobile')
    password = req_dict.get('password')

    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

    if not re.match(r'^1[3-9]\d{9}$', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='手机号格式不正确')

    # 2. 根据`手机号`查询User信息(如果查不到，说明用户不存在)
    try:
        user = User.query.filter(User.mobile == mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户信息失败')

    if not user:
        return jsonify(errno=RET.USERERR, errmsg='用户不存在')

    # 3. 校验用户的`密码`是否正确
    if not user.check_passowrd(password):
        return jsonify(errno=RET.PWDERR, errmsg='登录密码错误')

    # 4. 记住用户的登录状态
    session['user_id'] = user.id
    session['mobile'] = user.mobile
    session['nick_name'] = user.nick_name

    # 5. 返回应答，登录成功
    return jsonify(errno=RET.OK, errmsg='登录成功')


@passport_blu.route('/register', methods=['POST'])
def register():
    """
    用户注册:
    1. 接收参数(手机号，短信验证码，密码)并进行参数校验
    2. 根据`手机号`获取redis中短信验证码文本(如果取不到，说明短信验证码过期)
    3. 对比短信验证码，如果一致
    4. 创建User对象并保存注册用户的信息
    5. 将用户的注册信息添加进数据库
    6. 返回应答，注册成功
    """
    # 1. 接收参数(手机号，短信验证码，密码)并进行参数校验
    req_dict = request.json

    if not req_dict:
        return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')

    mobile = req_dict.get('mobile')
    sms_code = req_dict.get('sms_code')
    password = req_dict.get('password')

    if not all([mobile, sms_code, password]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

    if not re.match(r'^1[3-9]\d{9}$', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='手机号格式不正确')

    # 2. 根据`手机号`获取redis中短信验证码文本(如果取不到，说明短信验证码过期)
    try:
        real_sms_code = redis_store.get('sms_code:%s' % mobile)  # None
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='获取短信验证码失败')

    if not real_sms_code:
        return jsonify(errno=RET.NODATA, errmsg='短信验证码已过期')

    # 3. 对比短信验证码，如果一致
    if real_sms_code != sms_code:
        return jsonify(errno=RET.DATAERR, errmsg='短信验证码错误')

    # 4. 创建User对象并保存注册用户的信息
    user = User()
    user.mobile = mobile
    user.nick_name = mobile # 昵称默认为`手机号`
    user.password = password

    # 5. 将用户的注册信息添加进数据库
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存注册用户信息失败')

    # 6. 返回应答，注册成功
    return jsonify(errno=RET.OK, errmsg='注册成功')


@passport_blu.route('/sms_code', methods=['POST'])
def send_sms_code():
    """
    发送短信验证码:
    1. 接收参数(`手机号mobile`, `图片验证码image_code`, `图片验证码标识image_code_id`)并进行参数校验
    2. 根据`图片验证码标识image_code_id`从redis中获取真实的图片验证码文本(如果获取不到，图片验证码过期)
    3. 对比图片验证码文本，如果一致
    4. 使用云通讯给`手机号mobile`发送短信验证码
    5. 返回应答，发送短信成功
    """
    # 1. 接收参数(`手机号mobile`, `图片验证码image_code`, `图片验证码标识image_code_id`)并进行参数校验
    # 获取浏览器传递的json数据
    # json_data = request.data
    # 将json字符串转换成dict
    # req_dict = json.loads(json_data)

    # request.get_json()
    # 取浏览器传递的json数据并将json字符串转换成dict
    req_dict = request.json

    if not req_dict:
        return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')

    mobile = req_dict.get('mobile')
    image_code = req_dict.get('image_code')
    image_code_id = req_dict.get('image_code_id')

    if not all([mobile, image_code, image_code_id]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

    if not re.match(r'^1[3-9]\d{9}$', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='手机号格式不正确')

    # 2. 根据`图片验证码标识image_code_id`从redis中获取真实的图片验证码文本(如果获取不到，图片验证码过期)
    try:
        real_image_code = redis_store.get('image_code:%s' % image_code_id) # None
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='获取图片验证码失败')

    if not real_image_code:
        return jsonify(errno=RET.NODATA, errmsg='图片验证码已过期')

    # 3. 对比图片验证码文本，如果一致
    if real_image_code != image_code:
        return jsonify(errno=RET.DATAERR, errmsg='图片验证码错误')

    # 4. 使用云通讯给`手机号mobile`发送短信验证码
    # 4.1 随机生成一个6位数字
    sms_code = '%06d' % random.randint(0, 999999) # 000100
    current_app.logger.info('短信验证码为: %s' % sms_code)

    # 4.2 在redis中存储短信验证码内容，以`手机号mobile`为key，以`短信验证码内容`为value
    try:
        redis_store.set('sms_code:%s' % mobile, sms_code, constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存短信验证码失败')

    # 4.3 使用云通讯平台发送短信 13155667788
    # res = CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES/60], 1)
    #
    # if res != 0:
    #     return jsonify(errno=RET.THIRDERR, errmsg='发送短信失败')

    # 5. 返回应答，发送短信成功
    return jsonify(errno=RET.OK, errmsg='发送短信成功')


@passport_blu.route('/image_code')
def get_image_code():
    """
    产生图片验证码:
    1. 接收参数(图片验证码标识image_code_id)并且进行参数校验
    2. 产生图片验证码
    3. 在redis中保存验证码文本，以`图片验证码标识`为key，以验证码文本为value
    4. 返回验证码图片
    """
    # 1. 接收参数(图片验证码标识image_code_id)并且进行参数校验
    image_code_id = request.args.get('image_code_id')

    if not image_code_id:
        # abort(400)
        return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')

    # 2. 产生图片验证码
    # 图片名称 验证码文本 验证码图片内容
    name, text, content = captcha.generate_captcha()
    current_app.logger.info('图片验证码为: %s' % text)

    # 3. 在redis中保存验证码文本，以`图片验证码标识`为key，以验证码文本为value
    try:
        redis_store.set('image_code:%s' % image_code_id, text, constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存图片验证码失败')

    # 4. 返回验证码图片
    response = make_response(content)
    # 设置响应的数据类型
    response.headers['Content-Type'] = 'image/jpg'
    return response
