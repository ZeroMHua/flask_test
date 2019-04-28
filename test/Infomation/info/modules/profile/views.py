from flask import abort
from flask import current_app
from flask import g, jsonify
from flask import render_template
from flask import request
from flask import session

from info import constants
from info import db
from info.models import Category, News, User
from info.utils.commons import login_required
from info.utils.image_storage import storage
from info.utils.response_code import RET
from . import profile_blu


# /user/<int:user_id>/news?p=<page>
@profile_blu.route('/<int:user_id>/news')
@login_required
def user_others_news(user_id):
    """
    查询用户发布的新闻信息:
    """
    # 1. 获取页码并进行参数校验
    page = request.args.get('p', 1)

    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    # 2. 根据`user_id`查询用户的信息
    try:
        author = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户信息失败')

    if not author:
        return jsonify(errno=RET.NODATA, errmsg='用户不存在')
    
    # 3. 获取作者发布的新闻信息并进行分页
    try:
        pagination = author.news_list.filter(News.status == 0).paginate(page, constants.OTHER_NEWS_PAGE_MAX_COUNT, False)
        news_li = pagination.items
        total_page = pagination.pages
        current_page = pagination.page
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户发布新闻信息失败')

    news_dict_li = []
    for news in news_li:
        news_dict_li.append(news.to_basic_dict())
    
    # 4. 返回应答
    return jsonify(errno=RET.OK, errmsg='OK',
                   news_li=news_dict_li,
                   total_page=total_page,
                   current_page=current_page)


# /user/<int:user_id>
@profile_blu.route('/<int:user_id>')
@login_required
def user_others(user_id):
    """
    查看其他用户的页面:
    """
    # 获取登录的用户
    user = g.user

    # 根据`user_id`查询用户的信息
    try:
        author = User.query.get(user_id)
        author.avatar_url_path = constants.QINIU_DOMIN_PREFIX + author.avatar_url
    except Exception as e:
        current_app.logger.error(e)
        abort(500)

    if not author:
        abort(404)

    # 判断当前登录用户是否关注了author
    is_followed = False
    if user in author.followers:
        is_followed = True

    return render_template('news/other.html',
                           author=author,
                           user=user,
                           is_followed=is_followed)


# /user/follows
@profile_blu.route('/follows')
@login_required
def user_follows():
    """
    用户中心-我的关注页面
    """
    # 1. 接收参数并进行参数校验
    page = request.args.get('p', 1)

    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    # 2. 获取用户收藏的新闻信息并进行分页
    # 获取登录用户
    user = g.user
    try:
        pagination = user.followed.paginate(page, constants.USER_FOLLOWED_MAX_COUNT, False)
        follows = pagination.items
        total_page = pagination.pages
        current_page = pagination.page
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户收藏新闻信息失败')

    for followed_user in follows:
        followed_user.avatar_url_path = constants.QINIU_DOMIN_PREFIX + followed_user.avatar_url

    # 使用模板
    return render_template('news/user_follow.html',
                           follows=follows,
                           total_page=total_page,
                           current_page=current_page)


# /user/follow
@profile_blu.route('/follow', methods=['POST'])
@login_required
def user_follow():
    """
    关注和取消关注:
    1. 接收参数(user_id, action)并进行参数校验
    2. 根据`user_id`查询被关注用户的信息
    3. 根据action执行对应的操作
    4. 返回应答，关注或取消关注成功
    """
    # 1. 接收参数(user_id, action)并进行参数校验
    req_dict = request.json

    if not req_dict:
        return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')

    user_id = req_dict.get('user_id')
    action = req_dict.get('action')

    if not all([user_id, action]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

    try:
        user_id = int(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    if action not in ('do', 'undo'):
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    # 2. 根据`user_id`查询被关注用户的信息
    try:
        followed_user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户信息失败')

    if not followed_user:
        return jsonify(errno=RET.NODATA, errmsg='用户不存在')

    # 3. 根据action执行对应的操作
    user = g.user
    if action == 'do':
        # 关注
        if user not in followed_user.followers:
            followed_user.followers.append(user)
    else:
        # 取消关注
        if user in followed_user.followers:
            followed_user.followers.remove(user)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='操作失败')

    # 4. 返回应答，关注或取消关注成功
    return jsonify(errno=RET.OK, errmsg='操作成功')


# /user/news
@profile_blu.route('/news')
@login_required
def user_news_list():
    """
    用户中心-发布新闻列表页面:
    """
    # 1. 获取页码
    page = request.args.get('p', 1)

    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    # 2. 获取用户发布的新闻信息并进行分页处理
    user = g.user

    try:
        pagnation = user.news_list.paginate(page, constants.USER_COLLECTION_MAX_NEWS, False)
        news_li = pagnation.items
        total_page = pagnation.pages
        current_page = pagnation.page
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询收藏新闻失败')

    # 使用模板
    return render_template('news/user_news_list.html',
                           news_li=news_li,
                           total_page=total_page,
                           current_page=current_page)


# /user/release
@profile_blu.route('/release', methods=['GET', 'POST'])
@login_required
def user_news_release():
    """
    用户中心-发布信息页面:
    """
    if request.method == 'GET':
        # 获取所有`新闻分类`信息
        try:
            categories = Category.query.all()
        except Exception as e:
            current_app.logger.error(e)
            abort(500)

        # 去除`最新`分类
        categories.pop(0)

        # 使用模板
        return render_template('news/user_news_release.html', categories=categories)
    else:
        # 新闻发布处理
        # 1. 接收参数并进行参数校验
        title = request.form.get('title')
        category_id = request.form.get('category_id')
        digest = request.form.get('digest')
        content = request.form.get('content')
        file = request.files.get('index_image')
        
        if not all([title, category_id, digest, content, file]):
            return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')
        
        try:
            category_id = int(category_id)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

        # 2. 根据`category_id`去查询分类的信息
        try:
            category = Category.query.get(category_id)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg='查询分类信息失败')

        if not category:
            return jsonify(errno=RET.NODATA, errmsg='分类信息不存在')

        # 3. 将新闻的索引图片上传至七牛云
        try:
            key = storage(file.read())
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.THIRDERR, errmsg='上传图片失败')

        # 4. 创建News对象并保存新闻的信息
        news = News()
        news.title = title
        news.source = '个人发布'
        news.digest = digest
        news.content = content
        news.index_image_url = constants.QINIU_DOMIN_PREFIX + key
        news.category_id = category_id
        news.user_id = g.user.id
        news.status = 1 # 审核中

        try:
            db.session.add(news)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg='保存新闻信息失败')

        # 5. 返回应答，新闻发布成功
        return jsonify(errno=RET.OK, errmsg='新闻发布成功')


# /user/collection?p=页码
@profile_blu.route('/collection')
@login_required
def user_collection():
    """
    用户中心-我的收藏页面:
    """
    # 1. 获取页码
    page = request.args.get('p', 1)

    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    # 2. 获取用户收藏的新闻信息并进行分页处理
    user = g.user
    
    try:
        pagnation = user.collection_news.paginate(page, constants.USER_COLLECTION_MAX_NEWS, False)
        news_li = pagnation.items
        total_page = pagnation.pages
        current_page = pagnation.page
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询收藏新闻失败')


    # 使用模板
    return render_template('news/user_collection.html',
                           news_li=news_li,
                           total_page=total_page,
                           current_page=current_page)


# /user/password
@profile_blu.route('/password', methods=['GET', 'POST'])
@login_required
def user_password():
    """
    用户中心-修改密码页面:
    """
    if request.method == 'GET':
        return render_template('news/user_pass_info.html')
    else:
        # 进行修改密码的处理
        # 1. 接收参数并且进行校验
        req_dict = request.json

        if not req_dict:
            return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')

        old_password = req_dict.get('old_password')
        new_password = req_dict.get('new_password')

        if not all([old_password, new_password]):
            return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

        # 2. 判断用户输入旧密码是否正确
        user = g.user
        if not user.check_passowrd(old_password):
            return jsonify(errno=RET.DATAERR, errmsg='旧密码错误')

        # 3. 设置用户的新密码
        user.password = new_password

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg='保存密码失败')

        # 4. 返回应答，修改密码成功
        return jsonify(errno=RET.OK, errmsg='修改密码成功过')


# /user/avatar
@profile_blu.route('/avatar', methods=['GET', 'POST'])
@login_required
def user_avatar():
    """
    用户中心-个人头像页面:
    """
    # 从g变量中获取user
    user = g.user

    if request.method == 'GET':
        return render_template('news/user_pic_info.html', user=user)
    else:
        # 保存上传的用户头像
        # 1. 获取浏览器上传的头像文件
        file = request.files.get('avatar')

        if not file:
            return jsonify(errno=RET.PARAMERR, errmsg='缺少数据')

        # 2. 将头像文件上传到七牛云平台
        try:
            key = storage(file.read())
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.THIRDERR, errmsg='上传用户头像失败')

        # 3. 设置数据表中用户的头像地址
        user.avatar_url = key
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg='保存头像记录失败')
        
        # 4. 返回应答，上传头像成功
        avatar_url = constants.QINIU_DOMIN_PREFIX + key
        return jsonify(errno=RET.OK, errmsg='上传头像成功', avatar_url=avatar_url)


# /user/basic
@profile_blu.route('/basic', methods=['GET', 'POST'])
@login_required
def user_basic():
    """
    用户中心-基本信息页面:
    """
    # 从g变量中获取user
    user = g.user
    
    if request.method == 'GET':
        return render_template('news/user_base_info.html', user=user)
    else:
        # 保存修改用户的信息
        # 1. 接收参数并进行参数校验
        req_dict = request.json

        if not req_dict:
            return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')

        signature = req_dict.get('signature')
        nick_name = req_dict.get('nick_name')
        gender = req_dict.get('gender')

        if not all([signature, nick_name, gender]):
            return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

        if gender not in ('MAN', 'WOMAN'):
            return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

        # 2. 设置用户的个人信息
        user.signature = signature
        user.nick_name = nick_name
        user.gender = gender
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg='保存用户信息失败')

        # 设置session中的nick_name
        session['nick_name'] = nick_name
        
        # 3. 返回应答，设置个人信息成功
        return jsonify(errno=RET.OK, errmsg='设置个人信息成功')
            

@profile_blu.route('')
@login_required
def get_user_profile():
    """
    用户个人中心页面:
    """
    # 从g变量中获取user
    user = g.user

    return render_template('news/user.html', user=user)
