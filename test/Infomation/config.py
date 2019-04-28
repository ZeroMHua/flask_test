import logging
import redis


class Config(object):
    """项目的配置类"""

    # 设置SECRET_KEY
    SECRET_KEY = 'NmwKKxmKOSZrjTGVOI04o9RBj0/t3hcYDHFQ7TDD7zr803t+qMuKciveDNrot1Qd'

    # 数据库相关配置
    # 设置数据库的链接地址
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@172.16.179.139:3306/gz02_info'
    # 关闭追踪数据库的修改
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis数据库的相关配置
    REDIS_HOST = '172.16.179.139'
    REDIS_PORT = 6379

    # session存储的相关配置
    # 设置session存储到redis中
    SESSION_TYPE = 'redis'
    # redis链接对象(给flask-session扩展使用的)
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # 开启返回给浏览器cookie `session`值的加密
    SESSION_USE_SIGNER = True
    # 设置session过期时间
    PERMANENT_SESSION_LIFETIME = 24*3600*2


class DevelopmentConfig(Config):
    """开发环境中的配置类"""
    # 开启调试模式
    DEBUG = True
    # 开发环境中的日志等级
    LOG_LEVEL = logging.DEBUG


class ProductionConfig(Config):
    """生产环境(线上)中配置类"""
    # 配置生产环境中使用的配置类
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@172.16.179.139:3306/info'
    # 生产环境中的日志等级
    LOG_LEVEL = logging.WARNING

config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}