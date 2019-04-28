# 此文件中定义我们自己封装一些代码
import functools

from flask import abort
from flask import current_app, jsonify
from flask import g
from flask import redirect
from flask import session

from info import constants
from info.models import User
from info.utils.response_code import RET


def do_rank_class(index):
    """获取点击排行新闻对应class"""
    if index < 0 or index >= 3:
        return ''

    rank_class_li = ['first', 'second', 'third']

    return rank_class_li[index]


def do_news_status(status):
    assert status in [0, 1, -1], 'status必须在(0, 1, -1)中'

    status_dict = {
        0: '已通过',
        1: '审核中',
        -1: '未通过'
    }

    return status_dict[status]


def login_user_data(view_func):
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        # 尝试从session中获取user_id
        user_id = session.get('user_id')  # 获取不到，返回None

        user = None
        if user_id:
            # 用户已登录
            try:
                user = User.query.get(user_id)
                # 这句代码会出现bug，视图中commit的时候会把表中对应的用户的avatar_url改掉
                # user.avatar_url = constants.QINIU_DOMIN_PREFIX + user.avatar_url if user.avatar_url else ''

                # 给user对象增加一个属性avatar_url_path
                user.avatar_url_path = constants.QINIU_DOMIN_PREFIX + user.avatar_url if user.avatar_url else ''

                # if user.avatar_url:
                #     constants.QINIU_DOMIN_PREFIX + user.avatar_url
                # else:
                #     ''
            except Exception as e:
                current_app.logger.error(e)

        # 使用g变量临时保存user信息
        # g变量中保存的数据可以在请求开始到请求结束过程中的使用
        g.user = user

        return view_func(*args, **kwargs)

    return wrapper


def login_required(view_func):
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        # 尝试从session中获取user_id
        user_id = session.get('user_id')  # 获取不到，返回None
        
        if not user_id:
            # 用户未登录
            return jsonify(errno=RET.SESSIONERR, errmsg='用户未登录')

        # 用户已登录
        try:
            user = User.query.get(user_id)
            # 给user对象增加一个属性avatar_url_path
            user.avatar_url_path = constants.QINIU_DOMIN_PREFIX + user.avatar_url if user.avatar_url else ''
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg='获取用户信息失败')

        # 使用g变量临时保存user信息
        # g变量中保存的数据可以在请求开始到请求结束过程中的使用
        g.user = user

        return view_func(*args, **kwargs)

    return wrapper


def admin_login_required(view_func):
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        # 尝试从session中获取user_id
        user_id = session.get('user_id')
        is_admin = session.get('is_admin')

        if not user_id or not is_admin:
            # 登录用户不是管理员或用户未登录，直接跳转到首页
            return redirect('/')

        user = None
        try:
            user = User.query.get(user_id)
            user.avatar_url_path = constants.QINIU_DOMIN_PREFIX + user.avatar_url if user.avatar_url else ''
        except Exception as e:
            current_app.logger.error(e)
            abort(500)

        # 使用g变量临时保存user
        g.user = user

        return view_func(*args, **kwargs)
    return wrapper
