from flask import abort, jsonify
from flask import current_app
from flask import g
from flask import render_template
from flask import request
from flask import session

from info import constants, db
from info.models import User, News, Comment
from info.utils.commons import login_user_data, login_required
from info.utils.response_code import RET
from . import news_blu


@news_blu.route('/comment/like', methods=['POST'])
@login_required
def news_comment_like():
    """
    评论点赞或取消点赞:
    1. 接收参数(comment_id, action)并进行参数校验
    2. 根据`comment_id`去查询评论的信息(如果查不到，说明评论信息不存在)
    3. 根据action执行对应的操作
    4. 返回应答，评论点赞或取消点赞成功
    """
    # 1. 接收参数(comment_id, action)并进行参数校验
    req_dict = request.json

    if not req_dict:
        return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')

    comment_id = req_dict.get('comment_id')
    action = req_dict.get('action')

    if not all([comment_id, action]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

    if action not in ('do', 'undo'):
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    # 2. 根据`comment_id`去查询评论的信息(如果查不到，说明评论信息不存在)
    try:
        comment = Comment.query.get(comment_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询评论信息失败')

    if not comment:
        return jsonify(errno=RET.NODATA, errmsg='评论信息不存在')

    # 3. 根据action执行对应的操作
    user = g.user
    if action == 'do':
        # 3.1 如果action=='do', 进行`点赞`操作
        if comment not in user.like_comments:
            user.like_comments.append(comment)
            comment.like_count += 1
    else:
        # 3.2 如果action=='undo', 进行`取消点赞`操作
        if comment in user.like_comments:
            user.like_comments.remove(comment)
            comment.like_count -= 1
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='操作失败')

    # 4. 返回应答，评论点赞或取消点赞成功
    return jsonify(errno=RET.OK, errmsg='操作成功')


@news_blu.route('/comment', methods=['POST'])
@login_required
def save_news_comment():
    """
    评论新闻或回复评论:
    1. 接收参数(news_id, content, parent_id)并进行参数校验
    2. 根据`news_id`获取新闻的信息(如果查不到，说明新闻不存在)
    3. 创建Comment对象并保存`评论`信息
    4. 将`评论信息`添加进数据库
    5. 返回应答，评论新闻或回复评论成功
    """
    # 1. 接收参数(news_id, content, parent_id)并进行参数校验
    req_dict = request.json

    if not req_dict:
        return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')

    news_id = req_dict.get('news_id')
    content = req_dict.get('content')
    parent_id = req_dict.get('parent_id')

    if not all([news_id, content]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')
        
    try:
        news_id = int(news_id)
        if parent_id:
            parent_id = int(parent_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    # 2. 根据`news_id`获取新闻的信息(如果查不到，说明新闻不存在)
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询新闻信息失败')

    if not news:
        return jsonify(errno=RET.NODATA, errmsg='新闻不存在')

    # 3. 创建Comment对象并保存`评论`信息
    comment = Comment()
    comment.user_id = g.user.id
    comment.news_id = news_id
    comment.content = content

    if parent_id:
        comment.parent_id = parent_id

    # 新闻评论数量+1
    news.comments_count += 1

    # 4. 将`评论信息`添加进数据库
    try:
        db.session.add(comment)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存评论信息失败')
        
    # 5. 返回应答，评论新闻或回复评论成功
    return jsonify(errno=RET.OK, errmsg='OK', comment=comment.to_dict())


@news_blu.route('/collect', methods=['POST'])
@login_required
def news_collect():
    """
    新闻`收藏`或`取消收藏`
    1. 接收参数(news_id, action)并进行参数校验
    2. 根据`news_id`获取新闻的信息(如果查不到，说明新闻不存在)
    3. 根据action执行对应的操作
    4. 返回应答，收藏或取消收藏成功
    """
    # 获取登录的用户
    user = g.user

    # 1. 接收参数(news_id, action)并进行参数校验
    req_dict = request.json

    if not req_dict:
        return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')

    news_id = req_dict.get('news_id')
    action = req_dict.get('action')

    if not all([news_id, action]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

    if action not in ('do', 'undo'):
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    # 2. 根据`news_id`获取新闻的信息(如果查不到，说明新闻不存在)
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询新闻信息失败')

    if not news:
        return jsonify(errno=RET.NODATA, errmsg='新闻不存在')

    # 3. 根据action执行对应的操作
    if action == 'do':
        # 3.1 如果action=='do', 执行`收藏`操作
        if news not in user.collection_news:
            user.collection_news.append(news)
    else:
        # 3.2 如果action=='undo', 执行`取消收藏`操作
        if news in user.collection_news:
            user.collection_news.remove(news)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='操作失败')

    # 4. 返回应答，收藏或取消收藏成功
    return jsonify(errno=RET.OK, errmsg='操作成功')


# get_news_detail.__name__

@news_blu.route('/<int:news_id>')
@login_user_data
def get_news_detail(news_id):
    """
    新闻详情页面:
    """
    # 尝试从session中获取user_id
    # user_id = session.get('user_id')  # 获取不到，返回None
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

    # 根据`news_id`获取新闻详情信息
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        abort(404)

    if not news:
        abort(404)

    # 新闻`点击量`+1
    news.clicks += 1

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)

    # 获取`点击排行`的新闻信息
    rank_news_li = []
    try:
        rank_news_li = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS).all()
    except Exception as e:
        current_app.logger.error(e)

    # 判断用户｀是否收藏｀新闻
    is_collected = False
    if user:
        if news in user.collection_news:
            # 登录用户收藏了这个新闻
            is_collected = True

    # 获取当前新闻的`评论信息`
    comments_li = []
    try:
        comments_li = Comment.query.filter(Comment.news_id == news_id).order_by(Comment.create_time.desc()).all()
    except Exception as e:
        current_app.logger.error(e)

    # 获取用户点赞所有评论
    like_comments = []
    is_followed = False
    if user:
        like_comments = user.like_comments

        # 判断当前登录的用户是否关注了新闻作者
        if news.user and (user in news.user.followers):
            is_followed = True

    # 使用模板
    return render_template('news/detail.html',
                           user=user,
                           news=news,
                           rank_news_li=rank_news_li,
                           is_collected=is_collected,
                           comments_li=comments_li,
                           like_comments=like_comments,
                           qiniu_domain=constants.QINIU_DOMIN_PREFIX,
                           is_followed=is_followed)