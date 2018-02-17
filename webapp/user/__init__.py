# _*_ coding: utf-8 _*_
# filename: __init__.py
from flask import Blueprint
from webapp import login_manager
from webapp.models.userModel import User
_user = Blueprint('user', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get_or_404(user_id)


from . import view