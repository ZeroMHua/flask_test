from flask import current_app, jsonify
from flask import g
from flask import render_template
from flask import request
from flask import session

from info import constants
from info.models import User, News, Category
from info.utils.commons import login_user_data
from info.utils.response_code import RET
from . import index_blu
from info import redis_store


@index_blu.route('/news')
def get_news_list():
    """
    获取`分类新闻`列表信息:
    1. 接收参数并进行参数验证
    2. 根据`分类id`获取新闻的信息并进行分页
    3. 返回数据
    """
    # 1. 接收参数并进行参数验证
    category_id = request.args.get('cid')
    page = request.args.get('page', 1) # 如果获取不到page, get方法默认返回1
    per_page = request.args.get('per_page', constants.HOME_PAGE_MAX_NEWS)

    if not category_id:
        return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')

    try:
        category_id = int(category_id)
        page = int(page)
        per_page = int(per_page)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    # 2. 根据`分类id`获取新闻的信息并进行分页
    filters = [News.status == 0]
    # `最新`
    if category_id != 1:
        # 获取分类新闻的信息
        filters.append(News.category_id == category_id)

    try:
        pagination = News.query.filter(*filters).\
            order_by(News.create_time.desc()).\
            paginate(page, per_page, False) # 返回Pagination类的对象

        # 获取当前页的数据，items是list，items中每个元素都是以News实例对象
        news_li = pagination.items
        # 总页数
        total_page = pagination.pages
        # 当前页页码
        current_page = pagination.page
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='获取分类新闻信息失败')

    # 3. 返回数据
    # 遍历news_li将每个News实例对象转化成python字典
    news_dict_li = []
    for news in news_li:
        news_dict_li.append(news.to_basic_dict())

    return jsonify(errno=RET.OK,
                   errmsg='OK',
                   news_li=news_dict_li,
                   total_page=total_page,
                   current_page=page)


# 2. 使用蓝图对象注册路由
@index_blu.route('/', methods=['GET', 'POST'])
@login_user_data
def index():
    # 尝试从session中获取user_id
    # user_id = session.get('user_id') # 获取不到，返回None
    #
    # user = None
    # if user_id:
    #     # 用户已登录
    #     try:
    #         user = User.query.get(user_id)
    #         user.avatar_url = constants.QINIU_DOMIN_PREFIX + user.avatar_url
    #     except Exception as e:
    #         current_app.logger.error(e)

    # 从g变量中获取user
    user = g.user

    # 获取`点击排行`的新闻信息
    rank_news_li = []
    try:
        rank_news_li = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS).all()
    except Exception as e:
        current_app.logger.error(e)

    # 获取`新闻分类`的信息
    categories = []
    try:
        categories = Category.query.all()
    except Exception as e:
        current_app.logger.error(e)

    # 使用模板
    return render_template('news/index.html',
                           user=user,
                           rank_news_li=rank_news_li,
                           categories=categories)


# 当浏览器访问一个网站时，会默认访问网站下的路径/favicon.ico
# 目的就是获取网站图标文件
@index_blu.route('/favicon.ico')
def get_web_ico():
    """获取网站的图标"""
    # current_app.send_static_file: 获取静态目录下文件的内容
    # current_app.send_static_file('news/html/user.html')
    return current_app.send_static_file('news/favicon.ico')
