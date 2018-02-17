# _*_ coding: utf-8 _*_
# filename: view.py
from flask import render_template, redirect, url_for, flash, current_app, request
from .form import RegisterForm, LoginForm
from . import _user
from webapp import db
from webapp.models.userModel import User
from flask_login import login_user, logout_user, current_user, login_required
from webapp.mail import send_email
from ._function import ChangeAvatar


@_user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, \
                    password=form.password1.data, name=form.name.data, sex=form.sex.data)
        db.session.add(user)
        send_email(form.email.data, 'Josen博客网【邮箱验证】', 'email/email_confirmed',\
                   user=user, token=user.generate_confirmation_token())
        flash('验证邮件已发送至您的邮箱，请在验证邮件中获取激活链接')
        return redirect(url_for('user.login'))
    return render_template('user/register.html', form=form)


@_user.route('/confirmed/<token>')
@login_required
def confirmed(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('激活成功！')
        return redirect(url_for('main.index'))
    flash('该激活链接已过期！')
    return redirect(url_for('main.index'))


@_user.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed and request.endpoint[:5] != 'user.' and request.endpoint != 'static':
            return redirect(url_for('user.unconfirmed'))


@_user.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('user/unconfirmed.html')


@_user.route('/resend-email')
@login_required
def resend_email():
    send_email(current_user.email, 'Josen博客网【邮箱验证】', 'email/email_confirmed',
               user=current_user, token=current_user.generate_confirmation_token())
    flash('验证邮件重新已发送，请注意查收！')
    return redirect(url_for('main.index'))


@_user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.usernameEmail.data).first() \
               or User.query.filter_by(email=form.usernameEmail.data).first()
        if user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('登录成功')
            return redirect(url_for('main.index'))
        flash('用户名或密码有误！')
    return render_template('user/login.html', form=form)


@_user.route('/user-center/<id>')
@login_required
def user_center(id):
    user = User.query.get_or_404(id)
    return render_template('user/user_center.html', user=user)


@_user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已退出登录！')
    return redirect(url_for('main.index'))


@_user.route('/change-avatar', methods=['GET', 'POST'])
@login_required
def change_avatar():
    if request.method == 'POST':
        if ChangeAvatar.if_file_name(request.files['avatar'].filename):
            ChangeAvatar.change_avatar(request.files['avatar'], current_user.username)
            current_user.avatar_hash = ChangeAvatar.get_avatar_hash(current_user.username)
            db.session.add(current_user)
            flash('更新头像成功！')
            return redirect(url_for('.user_center', id=current_user.id))
        flash('请上传正确的图片格式！')
    return redirect(url_for('.user_center', id=current_user.id))


@_user.route('/change-info', methods=['GET', 'POST'])
@login_required
def change_info():
    if request.method == 'POST':
        current_user.name = request.form['name'] or current_user.name
        current_user.sex = request.form['sex'] or current_user.sex
        current_user.location = request.form['location'] or current_user.location
        current_user.about_me = request.form['about_me'] or current_user.about_me
        db.session.add(current_user)
    return redirect(url_for('.user_center', id=current_user.id))


@_user.route('/change-email')
@login_required
def change_email():


    return render_template('user/change_email.html')


@_user.route('/security-center')
@login_required
def security_center():


    return render_template('user/security_center.html')