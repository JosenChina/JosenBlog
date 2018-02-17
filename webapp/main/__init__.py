# _*_ coding: utf-8 _*_
# filename: __init__.py
from webapp.models.roleModel import Permission
from flask import Blueprint
_main = Blueprint('main', __name__)


from . import errors, view
@_main.app_context_processor
def inject_permission():
    return dict(Permission=Permission)
