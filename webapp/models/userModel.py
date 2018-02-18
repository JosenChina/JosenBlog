# _*_ coding: utf-8 _*_
# filename:userModel.py
from flask import current_app, url_for
from webapp import db, login_manager
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from . roleModel import Role, Permission
from .followModel import Follow


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
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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

    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    follower = db.relationship('Follow',
                               foreign_keys=[Follow.followed_id],
                               backref=db.backref('followed', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')

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
        return check_password_hash(self.password_hash, password)

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

    # 每次登录刷新一次登录项
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    # 查看用户是否有权限
    def can(self, permission):
        return self.role is not None and\
               (self.role.permissions & permission) == permission

    # 验证用户是否管理员
    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    # 生成更改邮箱密令
    def change_email_token(self, email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({
            'newEmail': email,
            'id': self.id
        })

    # 验证更改邮箱密令
    def change_email_confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('id') != self.id:
            return False
        self.email = data.get('email')
        db.session.add(self)
        return True

    # 修改密码
    def change_password(self, old_password, new_password):
        if not self.verify_password(old_password):
            return False
        self.password = new_password
        db.session.add(self)
        return True
