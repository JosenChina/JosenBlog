# _*_ coding: utf-8 _*_
# filename: errors.py
from . import _main
from flask import render_template


# 定义404页面
@_main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@_main.app_errorhandler(500)
def internal_server_errors(e):
    return render_template('500.html'), 500


@_main.app_errorhandler(403)
def server_refuse(e):
    return render_template('403.html'), 403

