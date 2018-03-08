# _*_ coding: utf-8 _*_
# filename:config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a string of hard to guess'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '【Josen的个人博客】'
    FLASKY_MAIL_SENDER = 'josenblog@josen.top'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtpdm.aliyun.com'
    MAIL_PORT = 25
    MAIL_USER_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    FLASKY_USER_CENTER_BLOGS_PER_PAGE = 20
    FLASKY_BLOGS_PER_PAGE = 20
    FLASKY_COMMENTS_PER_PAGE = 10
    FLASKY_FOLLOWED_PER_PAGE = 15
    FLASKY_HOTTEST_BLOGS = 20
    FLASKY_LAST_BLOGS = 40
    FLASKY_BLOGS_MANAGE_PER_PAGE = 30
    FLASKY_USERS_PER_PAGE = 100
    FLASKY_USERS_SEARCH_PER_PAGE = 10
    FLASKY_SEARCH_PER_PAGE = 20

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or\
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or\
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
