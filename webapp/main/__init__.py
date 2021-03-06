# _*_ coding: utf-8 _*_
# filename: __init__.py
from webapp.models.roleModel import Permission
from webapp.models.blogModel import Blog
from flask import Blueprint
from webapp.models import CommentReport
_main = Blueprint('main', __name__)


@_main.app_context_processor
def inject_permission():
    return dict(Permission=Permission, Blog=Blog, CommentReport=CommentReport)

from . import errors, view
