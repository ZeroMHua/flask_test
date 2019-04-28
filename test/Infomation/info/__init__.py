import logging
from logging.handlers import RotatingFileHandler

import redis
from flask import g
from flask import render_template
from flask import session
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_session import Session

from config import config_dict


# 创建SQLAlchemy的对象
db = SQLAlchemy()

redis_store = None


def setup_logging(log_level):
    # 设置日志的记录等级
    logging.basicConfig(level=log_level) # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=100*1024*1024, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


# 工厂方法
def create_app(config_name):
    # 创建Flask应用程序实例
    app = Flask(__name__)

    # 获取配置类
    config_cls = config_dict[config_name]

    # 项目日志设置
    setup_logging(config_cls.LOG_LEVEL)

    # 从配置类中加载配置信息
    app.config.from_object(config_cls)

    # db对象关联app
    db.init_app(app)

    # 创建redis链接对象
    global redis_store
    redis_store = redis.StrictRedis(host=config_cls.REDIS_HOST, port=config_cls.REDIS_PORT, decode_responses=True)

    # 为Flask项目开启CSRF保护
    # CSRFProtect只做保护验证工作，所有我们之后需要自己完成2步:
    # 1. 在服务器端生成crsf_token并且把它保存起来
    # 2. 告诉浏览器生成的csrf_token，浏览器发起请求时需要把csrf_token带上
    CSRFProtect(app)

    # pip install flask-session
    # session存储设置
    Session(app)

    @app.after_request
    def after_request(response):
        # 1. 在服务器端生成crsf_token并且把它保存起来
        from flask_wtf.csrf import generate_csrf
        csrf_token = generate_csrf()
        # 2. 告诉浏览器生成的csrf_token
        response.set_cookie('csrf_token', csrf_token)

        return response

    # 添加自定义的过滤器
    from ..info.utils.commons import do_rank_class, do_news_status
    app.add_template_filter(do_rank_class, 'rank_class')
    app.add_template_filter(do_news_status, 'news_status')

    from ..info.utils.commons import login_user_data

    # 自定义处理404错误
    @app.errorhandler(404)
    @login_user_data
    def handle_page_not_found(e):
        # 从g变量中获取user
        user = g.user
        return render_template('news/404.html', user=user)

    # 3. 使用app对象注册蓝图
    from ..info.modules.index import index_blu
    from ..info.modules.passport import passport_blu
    from ..info.modules.news import news_blu
    from ..info.modules.profile import profile_blu
    from ..info.modules.admin import admin_blu
    app.register_blueprint(index_blu)
    app.register_blueprint(passport_blu, url_prefix='/passport')
    app.register_blueprint(news_blu, url_prefix='/news')
    app.register_blueprint(profile_blu, url_prefix='/user')
    app.register_blueprint(admin_blu, url_prefix='/admin')

    return app
