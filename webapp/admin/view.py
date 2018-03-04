# _*_ coding: utf-8 _*_
# filename: view.py

from flask import render_template, redirect, flash, url_for
from flask_login import login_required, current_user
from . import _admin
from ..models.commentModel import Comment
from webapp import db
from webapp.decorators import admin_required


@_admin.route('/comment-enable/<int:bid>/<page>/<int:id>')
@login_required
@admin_required
def comment_enable(bid, page, id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    flash('已启用！')
    return redirect(url_for('main.look_blog', id=bid, page=page))


@_admin.route('/comment-disable/<int:bid>/<page>/<int:id>')
@login_required
@admin_required
def comment_disable(bid, page, id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    flash('已禁用！')
    return redirect(url_for('main.look_blog', id=bid, page=page))

