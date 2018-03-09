# _*_ coding: utf-8 _*_
# filename: form.py
from flask_login import current_user
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


class ChangeEmailForm(FlaskForm):
    password = PasswordField('密码', validators=[DataRequired('请输入当前用户密码！')])
    email = StringField('新邮箱', validators=[Email('邮箱格式输入有误！')])
    submit = SubmitField('发送验证邮件')

    def validate_password(self, field):
        if not current_user.verify_password(field.data):
            raise ValidationError('密码输入有误！')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已绑定其他账号，请输入未绑定的邮箱！')


class ChangePasswordForm(FlaskForm):
    oldPassword = PasswordField('原密码', validators=[DataRequired('请输入当前账户的旧密码！')])
    newPassword1 = PasswordField('新密码', validators=[Length(1, 64, message='密码长度请不要超出64位！'),\
                                                    DataRequired('请输入新密码！'), Regexp('^[A-Za-z0-9_@]*$',\
                                                    message='请不要输入字母、数字、下划线、“@”以外的字符！')])
    newPassword2 = PasswordField('确认密码', validators=[EqualTo('newPassword1', message='两次密码输入不一致！')])
    submit = SubmitField('确认修改')

    def validate_oldPassword(self, field):
        if not current_user.verify_password(field.data):
            raise ValidationError('原密码输入不正确！')


class ForgetForm(FlaskForm):
    email = StringField('账户绑定邮箱邮箱', validators=[DataRequired('此处不能为空！'), Email('请输入正确的邮箱格式')])
    passwd1 = PasswordField('输入新密码', validators=[DataRequired('此处不能为空')])
    passwd2 = PasswordField('确认密码', validators=[EqualTo('passwd1', message='两次密码输入不一致！')])
    submit = SubmitField('提交')

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱不存在！请重新注册！')