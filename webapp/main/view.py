# _*_ coding: utf-8 _*_
# filename: view.py
from . import _main
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, flash, request, session, abort, current_app, make_response
from webapp.decorators import permission_required, admin_required
from webapp import db
from ..models.userModel import User
from ..models.roleModel import Permission
from ..models.blogModel import Blog
from ..models.commentModel import Comment
from datetime import datetime
from random import randint
import os
from ._function import delete_blog_imgs


@_main.route('/')
def index():
    # 我关注的列表
    followed_pagination = None
    # 我最近发表过的三篇博客
    fbn = 0
    FB3 = None
    # 最热的20篇文章
    hottest_blogs = Blog.query.order_by(Blog.looks.desc()).limit(current_app.config['FLASKY_HOTTEST_BLOGS'])
    # 最近发表40篇博客
    last_blogs = Blog.query.order_by(Blog.timestamp.desc()).limit(current_app.config['FLASKY_LAST_BLOGS'])
    # 我的评论管理
    cn = None
    comments_pagination = None
    with open('%s/../admin/bulletin.txt' % os.path.dirname(__file__), 'r') as f:
        bulletin = f.read()
    if current_user.is_authenticated:
        followed_page = request.args.get('_page', 1, type=int)
        followed_pagination = current_user.followed.paginate(
            followed_page, per_page=current_app.config['FLASKY_FOLLOWED_PER_PAGE'],
            error_out=False
        )
        # 最近发表的三篇文章
        FB3 = Blog.query.filter(Blog.author_id == current_user.id).order_by(Blog.timestamp.desc()).limit(3)
        fbn=FB3.count()
        comments_page = request.args.get('comments_page', 1, type=int)
        Comments = Comment.query.filter(Comment.author_id == current_user.id)
        cn = Comments.count()
        comments_pagination = Comments.order_by(Comment.timestamp.desc()).paginate(comments_page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'], error_out=False)

    return render_template('main/index.html', fbn=fbn, FB3=FB3, comments_pagination=comments_pagination, cn=cn,
                           hottest_blogs=hottest_blogs, comments_pagination_view='main.index',
                           last_blogs=last_blogs, bulletin=bulletin,
                           followed_pagination=followed_pagination, randint=randint)


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


@_main.route('/edit-blog', methods=['GET', 'POST'])
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
    return render_template('main/postBlog.html', bid=blog.id,
                           first_content=blog.body_html, action=url_for('main.edit_blog'), title=blog.title)


@_main.route('cancel-blog/<bid>')
@login_required
@permission_required(Permission.WRITE_ARTICLES)
def cancel_blog(bid):
    blog = Blog.query.get_or_404(bid)
    if blog.author_id == current_user.id:
        delete_blog_imgs(blog)
        for comment in blog.comments:
            db.session.delete(comment)
        for i in blog.imgs:
            db.session.delete(i)
        db.session.delete(blog)
        db.session.commit()
    session['blog_id'] = None
    return redirect(url_for('main.index'))


@_main.route('/look-blog/<int:id>', methods=['GET', 'POST'])
def look_blog(id):
    blog = Blog.query.get_or_404(id)
    blog.ping()
    moderate = current_user.is_authenticated and (blog.author_id == current_user.id or current_user.is_administrator())
    page = request.args.get('page', 1, type=int)
    comments_pagination = blog.comments.order_by(Comment.timestamp.desc())\
        .paginate(page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'], error_out=False)
    return render_template('main/lookBlog.html', comments_pagination=comments_pagination,
                           blog=blog, moderate=moderate, comments_pagination_view='main.look_blog')


@_main.route('/change-blog/<int:id>')
@login_required
@permission_required(Permission.WRITE_ARTICLES)
def change_blog(id):
    blog = Blog.query.get_or_404(id)
    if not blog:
        abort(404)
    if not current_user.is_administrator() and blog.author_id != current_user.id:
        abort(403)
    session['blog_id'] = id
    return redirect(url_for('main.edit_blog'))


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

#
# @_main.route('/comment-moderate')
# @login_required
# @permission_required(Permission.MODERATE_COMMENTS)
# def moderate():
#     page = request.args.get('comments_page', 1, type=int)
#     Comments = Comment.query.filter(Comment.author_id == current_user.id).order_by(Comment.timestamp.desc())
#     pagination = Comments.paginate(page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'], error_out=False)
#     return render_template('main/myComments.html', moderate=True, cn=Comments.count(),
#                            comments=pagination.items, pagination=pagination)


@_main.route('/delete-comment/<id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    if current_user == comment.author:
        db.session.delete(comment)
        flash('已删除！')
    return '<script>self.location=document.referrer</script>'


@_main.route('/blogs-manage')
@login_required
@permission_required(Permission.WRITE_ARTICLES)
def blogs_manage():
    page = request.args.get('blogs_page', 1, type=int)
    Blogs = Blog.query.filter(Blog.author_id == current_user.id)
    pagination = Blogs.paginate(page, per_page=current_app.config['FLASKY_BLOGS_MANAGE_PER_PAGE'], error_out=False)
    bn = Blogs.count()
    return render_template('main/blogsManage.html', pagination=pagination,
                           randint=randint, bn=bn, endpoint='main.blogs_manage')


@_main.route('/delete-blog/<id>')
@login_required
@permission_required(Permission.WRITE_ARTICLES)
def delete_blog(id):
    blog = Blog.query.get_or_404(id)
    if blog.author_id != current_user.id and not current_user.is_administrator():
        abort(403)
    delete_blog_imgs(blog)
    for comment in blog.comments:
        db.session.delete(comment)
    for i in blog.imgs:
        db.session.delete(i)
    db.session.delete(blog)
    db.session.commit()
    session['blog_id'] = None
    return redirect(url_for('main.blogs_manage'))


@_main.route('/search', methods=['GET', 'POST'])
def search():
    if request.method != 'POST':
        abort(403)
    mkp = make_response(redirect(url_for('main.search_results', search=request.form['search'])))
    mkp.set_cookie('search', request.form['search'], max_age=60*60)
    return mkp


@_main.route('/search-results')
def search_results():
    page = request.args.get('comments_page', 1, type=int)
    pagination = Blog.query.filter(
        Blog.title.like(
            '%'+(request.args.get('search'+'%') or request.cookies.get('search'))+'%'
        )).paginate(
        page, current_app.config['FLASKY_SEARCH_PER_PAGE'], error_out=False
    )
    return render_template('main/search.html',
                           pagination=pagination, endpoint='main.search_results')
