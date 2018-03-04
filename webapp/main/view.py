# _*_ coding: utf-8 _*_
# filename: view.py
from . import _main
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, flash, request, session, abort, current_app
from webapp.decorators import permission_required, admin_required
from webapp import db
from ..models.userModel import User
from ..models.roleModel import Role, Permission
from ..models.blogModel import Blog
from ..models.commentModel import Comment
from ..models.followModel import Follow
from datetime import datetime
from random import randint


@_main.route('/')
def index():
    followed_pagination = None
    if current_user.is_authenticated:
        followed_page = request.args.get('_page', 1, type=int)
        followed_pagination = current_user.followed.paginate(
            followed_page, per_page=current_app.config['FLASKY_FOLLOWED_PER_PAGE'],
            error_out=False
        )

    return render_template('main/index.html', followed_pagination=followed_pagination)


@_main.route('/following/<int:id>')
@login_required
def follow(id):
    user = User.query.get_or_404(id)
    if current_user.can(Permission.FOLLOW) and current_user.following(user):
        flash('关注成功！')
    return redirect(url_for('user.user_center', id=user.id))


@_main.route('/cancel-following/<int:id>')
@login_required
def unfollow(id):
    user = User.query.get_or_404(id)
    if current_user.cancel_follow(user):
        flash('已取消关注！')
    return redirect(url_for('user.user_center', id=user.id))


@_main.route('/post-blog', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.WRITE_ARTICLES)
def edit_blog():
    if not session.get('blog_id'):
        blog = Blog(author=current_user._get_current_object())
        db.session.add(blog)
        db.session.commit()
        session['blog_id'] = blog.id
    else:
        blog = Blog.query.filter_by(id=session.get('blog_id')).first()
    if request.method == 'POST':
        blog.body = request.form['blog_content']
        blog.title = (request.form['title'] or u'暂无标题')\
                     + '+-+' + (session.get('blog_avatar') or
                                url_for('static', filename='blog_avatar/%s.jpg' % randint(1, 8), _external=True))
        blog.timestamp = datetime.utcnow()
        blog.looks = 0
        db.session.add(blog)
        session['blog_id'] = None
        session['blog_avatar'] = None
        return redirect(url_for('main.index'))
    return render_template('main/postBlog.html',
                           first_content=blog.body_html, action=url_for('main.edit_blog'), title=blog.title)


@_main.route('/look-blog/<int:id>', methods=['GET', 'POST'])
def look_blog(id):
    blog = Blog.query.get_or_404(id)
    blog.ping()
    moderate = blog.author_id == current_user.id or current_user.is_administrator()
    page = request.args.get('page', 1, type=int)
    pagination = blog.comments.order_by(Comment.timestamp.desc())\
        .paginate(page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'], error_out=False)
    comments = pagination.items
    return render_template('main/lookBlog.html', pagination=pagination,
                           blog=blog, comments=comments, moderate=moderate)


@_main.route('/change-blog/<int:id>')
@login_required
@permission_required(Permission.WRITE_ARTICLES)
def change_blog(id):
    if Blog.query.get_or_404(id):
        session['blog_id'] = id
        return redirect(url_for('main.edit_blog'))
    flash('暂时无法修改！')
    return redirect(url_for('main.look_blog', id=id))


@_main.route('/comment-blog/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def comment_blog(id):
    if request.method == 'POST':
        db.session.add(Comment(body=request.form['body'],
                               author=current_user._get_current_object(), blog=Blog.query.get_or_404(id)))
        flash('已评论！')
    return redirect(url_for('main.look_blog', id=id)+'#comments')


@_main.route('/comment-enable/<int:bid>/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def comment_enable(bid, id):
    page = request.args.get('page', 1, type=int)
    blog = Blog.query.get_or_404(bid)
    if blog.author != current_user and not current_user.is_administrator():
        abort(403)
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    flash('已启用！')
    return redirect(url_for('main.look_blog', id=bid, page=page))


@_main.route('/comment-disable/<int:bid>/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def comment_disable(bid, id):
    page = request.args.get('page', 1, type=int)
    blog = Blog.query.get_or_404(bid)
    if blog.author != current_user and not current_user.is_administrator():
        abort(403)
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    flash('已禁用！')
    return redirect(url_for('main.look_blog', id=bid, page=page))


@_main.route('/comment-moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    page = request.args.get('page', 1, type=int)
    Comments = Comment.query.filter(Comment.author_id == current_user.id).order_by(Comment.timestamp.desc())
    pagination = Comments.paginate(page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'], error_out=False)
    return render_template('main/myComments.html', moderate=True, cn=Comments.count(),
                           comments=pagination.items, pagination=pagination)


@_main.route('/delete-comment/<id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    if current_user == comment.author:
        db.session.delete(comment)
        flash('已删除！')
    return '<script>self.location=document.referrer</script>'
