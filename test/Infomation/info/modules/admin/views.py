from datetime import datetime, timedelta

from flask import abort
from flask import current_app, jsonify
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from info import constants
from info.models import User, News, Category
from info.utils.commons import admin_login_required
from info.utils.image_storage import storage
from info.utils.response_code import RET
from . import admin_blu

from info import db
from sqlalchemy import extract


@admin_blu.route('/news/types/edit', methods=['POST'])
@admin_login_required
def news_type_edit():
    """
    后台管理-分类信息添加或修改:
    """
    # 1. 获取数据并进行数据校验
    req_dict = request.json

    if not req_dict:
        return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')

    category_id = req_dict.get('id')
    name = req_dict.get('name')

    if not name:
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

    # 2. 根据category_id获取分类信息
    if category_id:
        try:
            category_id = int(category_id)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

        try:
            category = Category.query.get(category_id)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg='查询分类信息失败')

        if not category:
            return jsonify(errno=RET.NODATA, errmsg='分类信息不存在')

    # 3. 执行添加或者修改操作
    if category_id:
        # 修改
        category.name = name
    else:
        # 添加
        category = Category()
        category.name = name
        
    try:
        db.session.add(category)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='操作失败')

    # 4. 返回应答，操作成功
    return jsonify(errno=RET.OK, errmsg='操作成功')


@admin_blu.route('/news/types')
@admin_login_required
def news_types():
    """
    后台管理-分类页面显示:
    """
    # 获取所有分类的信息
    try:
        categories = Category.query.all()
    except Exception as e:
        current_app.logger.error(e)
        abort(500)

    # 去除最新分类
    categories.pop(0)

    # 使用模板
    return render_template('admin/news_type.html', categories=categories)


@admin_blu.route('/news/edit/<int:news_id>', methods=['GET', 'POST'])
@admin_login_required
def news_edit_detail(news_id):
    """
    后台管理-新闻编辑详情页面:
    """
    if request.method == 'GET':
        # 1. 根据`news_id`查询新闻信息
        try:
            news = News.query.get(news_id)
        except Exception as e:
            current_app.logger.error(e)
            abort(500)

        if not news:
            # 新闻信息不存在
            abort(404)

        # 2. 获取所有分类的信息
        try:
            categories = Category.query.all()
        except Exception as e:
            current_app.logger.error(e)
            abort(500)

        # 去除最新分类
        categories.pop(0)

        # 3. 使用模板
        return render_template('admin/news_edit_detail.html',
                               news=news,
                               categories=categories)
    else:
        # 执行编辑处理
        # 1. 接收参数并进行参数校验
        title = request.form.get("title")
        digest = request.form.get("digest")
        content = request.form.get("content")
        index_image = request.files.get("index_image")
        category_id = request.form.get("category_id")

        if not all([title, digest, content, category_id]):
            return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

        try:
            category_id = int(category_id)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

        # 2. 根据`news_id`获取新闻信息
        try:
            news = News.query.get(news_id)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg='查询新闻信息失败')

        if not news:
            # 没有这个新闻
            return jsonify(errno=RET.NODATA, errmsg='新闻信息不存在')

        # 3. 如果上传了索引图片，将图片上传至七牛云平台
        if index_image:
            try:
                key = storage(index_image.read())
            except Exception as e:
                current_app.logger.error(e)
                return jsonify(errno=RET.THIRDERR, errmsg='上传文件到七牛云失败')

        # 4. 设置新闻的信息并保存
        news.title = title
        news.digest = digest
        news.content = content
        news.category_id = category_id

        if index_image:
            news.index_image_url = constants.QINIU_DOMIN_PREFIX + key

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg='保存新闻信息失败')

        # 5. 返回应答，编辑成功
        return jsonify(errno=RET.OK, errmsg='编辑成功')


@admin_blu.route('/news/edit')
@admin_login_required
def news_edit():
    """
    后台管理-新闻编辑页面:
    """
    # 1. 获取参数并进行校验
    page = request.args.get('p', 1)
    key = request.args.get('key')

    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        abort(404)

    # 2. 获取所有新闻信息
    filters = []

    if key:
        filters.append(News.title.contains(key))

    try:
        pagination = News.query.filter(*filters). \
            order_by(News.create_time.desc()). \
            paginate(page, constants.ADMIN_NEWS_PAGE_MAX_COUNT, False)
        news_li = pagination.items
        total_page = pagination.pages
        current_page = pagination.page
    except Exception as e:
        current_app.logger.error(e)
        abort(500)

    return render_template('admin/news_edit.html',
                           news_li=news_li,
                           total_page=total_page,
                           current_page=current_page)


@admin_blu.route('/news/review/<int:news_id>', methods=['GET', 'POST'])
@admin_login_required
def news_review_detail(news_id):
    """
    后台管理-新闻审核详情页面:
    """
    if request.method == 'GET':
        # 1. 根据`news_id`获取新闻信息
        try:
            news = News.query.get(news_id)
        except Exception as e:
            current_app.logger.error(e)
            abort(500)

        if not news:
            # 没有这个新闻
            abort(404)
        # 2. 使用模板
        return render_template('admin/news_review_detail.html', news=news)
    else:
        # 执行审核操作
        # 1. 获取参数并进行参数校验
        req_dict = request.json
        if not req_dict:
            return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')

        action = req_dict.get('action')

        if not action:
            return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

        if action not in ('accept', 'reject'):
            return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

        # 2. 根据`news_id`获取新闻信息
        try:
            news = News.query.get(news_id)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg='查询新闻信息失败')

        if not news:
            # 没有这个新闻
            return jsonify(errno=RET.NODATA, errmsg='新闻信息不存在')

        # 3. 根据action执行对应的操作:
        if action == 'accept':
            # 审核通过
            news.status = 0
        else:
            # 拒绝通过
            news.status = -1
            
            # 获取拒绝原因
            reason = req_dict.get('reason')
            
            if not reason:
                return jsonify(errno=RET.PARAMERR, errmsg='缺少拒绝原因')

            news.reason = reason
            
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg='操作失败')
        
        # 4. 返回应答，审核成功
        return jsonify(errno=RET.OK, errmsg='审核成功')


@admin_blu.route('/news/review')
@admin_login_required
def news_review():
    """
    后台管理-新闻审核列表页面:
    """
    # 1. 获取参数并进行校验
    page = request.args.get('p', 1)
    key = request.args.get('key')

    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        abort(404)

    # 2. 获取所有新闻的信息并进行分页
    filters = []
    if key:
        filters.append(News.title.contains(key))

    try:
        pagination = News.query.filter(*filters). \
            order_by(News.create_time.desc()). \
            paginate(page, constants.ADMIN_NEWS_PAGE_MAX_COUNT, False)

        news_li = pagination.items
        total_page = pagination.pages
        current_page = pagination.page
    except Exception as e:
        current_app.logger.error(e)
        abort(500)

    # 3. 使用模板
    return render_template('admin/news_review.html',
                           news_li=news_li,
                           total_page=total_page,
                           current_page=current_page)


@admin_blu.route('/user/list')
@admin_login_required
def user_list():
    """
    后台管理-用户列表信息页面:
    """
    # 1. 获取参数并进行校验
    page = request.args.get('p', 1)

    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        abort(404)

    # 2. 获取所有普通用户信息并进行分页
    try:
        pagination = User.query.order_by(User.create_time.desc()). \
            paginate(page, constants.ADMIN_USER_PAGE_MAX_COUNT, False)
        users = pagination.items
        total_page = pagination.pages
        current_page = pagination.page
    except Exception as e:
        current_app.logger.error(e)
        abort(500)

    # 3. 使用模板文件
    return render_template('admin/user_list.html',
                           users=users,
                           total_page=total_page,
                           current_page=current_page)


# /admin/user/count
@admin_blu.route('/user/count')
@admin_login_required
def user_count():
    """
    后台管理-用户统计页面:
    """
    # 统计网站用户的总数
    total_count = User.query.count()

    # 统计当月用户的新增数量
    now_date = datetime.now()  # datetime
    year = now_date.year
    month = now_date.month

    month_count = db.session.query(User).filter(extract('year', User.create_time) == year,
                                                extract('month', User.create_time) == month).count()

    # 统计当天用户的新增数量
    day = now_date.day
    day_count = db.session.query(User).filter(extract('year', User.create_time) == year,
                                              extract('month', User.create_time) == month,
                                              extract('day', User.create_time) == day).count()

    # 统计最近30天每天用户新增数量
    counts_li = []
    date_li = []
    begin_date = now_date - timedelta(days=29)

    for i in range(0, 30):
        # 计算当前日期
        cur_date = begin_date + timedelta(days=i)

        # 获取当前日期的年月日
        year = cur_date.year
        month = cur_date.month
        day = cur_date.day

        # 计算出当天新增用户数量
        count = db.session.query(User).filter(extract('year', User.create_time) == year,
                                              extract('month', User.create_time) == month,
                                              extract('day', User.create_time) == day).count()

        # 把当天新增用户数量保存在counts_li列表中
        counts_li.append(count)

        # 保存当前日期
        date_str = cur_date.strftime('%Y-%m-%d')
        date_li.append(date_str)

    return render_template('admin/user_count.html',
                           total_count=total_count,
                           month_count=month_count,
                           day_count=day_count,
                           counts_li=counts_li,
                           date_li=date_li)


# /admin/logout
@admin_blu.route('/logout', methods=['POST'])
def logout():
    """
    管理员退出登录:
    1. 清除session对应的登录信息
    2. 返回应答，退出成功
    """
    # 1. 清除session对应的登录信息
    session.pop('user_id')
    session.pop('mobile')
    session.pop('nick_name')
    session.pop('is_admin')

    # 2. 返回应答，退出成功
    return jsonify(errno=RET.OK, errmsg='退出成功')


# /admin/index
@admin_blu.route('/index')
@admin_login_required
def index():
    """
    后台管理首页:
    """
    # 获取当前登录用户user
    user = g.user

    return render_template('admin/index.html', user=user)


# /admin/login
@admin_blu.route('/login', methods=['GET', 'POST'])
def login():
    """
    后台管理员登录页面:
    """
    if request.method == 'GET':
        # 显示页面
        user_id = session.get('user_id')
        is_admin = session.get('is_admin')

        if user_id and is_admin:
            # 管理员已登录
            return redirect(url_for('admin.index'))

        return render_template('admin/login.html')
    else:
        # 进行登录处理
        # 1. 接收参数并进行参数校验
        username = request.form.get('username')
        password = request.form.get('password')

        if not all([username, password]):
            flash('参数不完整')
            # 重定向的请求方式是GET
            return redirect(url_for('admin.login'))

        # 2. 根据`username`去查询管理员用户的信息
        try:
            user = User.query.filter(User.nick_name == username,
                                     User.is_admin == True).first()
        except Exception as e:
            current_app.logger.error(e)
            flash('服务器错误')
            return redirect(url_for('admin.login'))

        if not user:
            flash('用户不存在')
            return redirect(url_for('admin.login'))

        # 3. 校验用户的登录密码是否正确
        if not user.check_passowrd(password):
            flash('密码错误')
            return redirect(url_for('admin.login'))

        # 4. 在session中记住用户的登录状态
        session['user_id'] = user.id
        session['nick_name'] = user.nick_name
        session['mobile'] = user.mobile
        session['is_admin'] = True

        # 5. 登录成功，跳转到后台管理的首页
        # return '后台管理首页'
        return redirect(url_for('admin.index'))
