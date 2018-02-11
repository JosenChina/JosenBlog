# _*_ coding: utf-8 _*_
# filename:userModel.py
from flask import current_app, url_for
from webapp import db, login_manager
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from . roleModel import Role


class AnonymousUser(AnonymousUserMixin):
    # 未登录用户类
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


# 将未登录用户类注册到程序登录管理进程
login_manager.anonymous_user = AnonymousUser


# 用户类
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64))
    sex = db.Column(db.String(4))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow())
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow())
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)
    avatar_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User %r>' % self.username

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            else:
                self.role = Role.query.filter_by(default=True).first()
        if self.avatar_hash is None:
            # 设置头像默认地址
            if self.sex == '男':
                self.avatar_hash = url_for('static', filename='default_avatar_m.png', _external=True)
            elif self.sex == '女':
                self.avatar_hash = url_for('static', filename='default_avatar_w.png', _external=True)

    # 将password属性设置为不可获取
    @property
    def password(self):
        raise AttributeError('该属性不被显示')

    # 当改变password时自动触发，改变对应的password_hash属性，生成password的hash值
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 验证密码是否匹配对应的hash值
    def verify_password(self, password):
        return check_password_hash(self.passwd_hash, password)

    # 生成密令
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    # 解密密令
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True