# _*_ coding: utf-8 _*_
# filename: view.py

from flask import render_template, redirect, flash, url_for, request
from flask_login import login_required, current_user
from . import _admin
from ._function import clean
from ..models.commentModel import Comment
from webapp import db
from webapp.decorators import admin_required
import os


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


@_admin.route('/edit-bulletin', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_bulletin():
    bulletin = None
    with open('%s/bulletin.txt' % os.path.dirname(__file__), 'r') as f:
        bulletin = f.read()
    if request.method == 'POST':
        with open('%s/bulletin.txt' % os.path.dirname(__file__), 'w') as f:
            f.write(clean(request.form['bulletin']))
            # f.write(request.form['bulletin'])
        return redirect(url_for('main.index'))
    return render_template('admin/editBulletin.html', bulletin=bulletin)
