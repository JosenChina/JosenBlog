# _*_ coding: utf-8 _*_
# filename: form.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Regexp, Length, EqualTo
from wtforms.validators import ValidationError
from webapp.models.userModel import User


class RegisterForm(FlaskForm):
    username = StringField('用户名', \
                           validators=[DataRequired(message='用户名不能为空！'),\
                                       Length(1, 64, message='长度不能超过64位'),\
                                       Regexp('^[A-Za-z][A-Za-z0-9_]*$', message='请输入字母开头的用户名，不要输入字母数字下划线以外的字符！')])
    email = StringField('邮箱',\
                        validators=[DataRequired(message='请输入邮箱！'),\
                                    Length(1, 128, message='长度超过邮箱范围'),\
                                    Email(message='邮箱格式输入有误！')])
    password1 = PasswordField('密码', validators=[DataRequired('请输入密码')])
    password2 = PasswordField('确认密码', validators=[EqualTo('password1', message='两次密码输入不一致！')])
    name = StringField('姓名', validators=[DataRequired('请输入姓名！'), Length(1, 64, message='长度不能超过64位')])
    sex = RadioField('性别', choices=[('男','男'), ('女', '女')], default='男')
    submit = SubmitField('注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已被注册！')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册！')


class LoginForm(FlaskForm):
    usernameEmail = StringField('请输入用户名或邮箱', validators=[DataRequired('请输入用户名或邮箱！')])
    password = PasswordField('密码', validators=[DataRequired('请输入密码！')])
    remember_me = BooleanField('记住密码')
    submit = SubmitField('登录')

    def validate_usernameEmail(self, field):
        if not User.query.filter_by(username=field.data).first() and not User.query.filter_by(email=field.data).first():
            raise ValidationError('该用户名或邮箱不存在！')

