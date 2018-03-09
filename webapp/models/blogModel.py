# _*_ coding: utf-8 _*_
# filename: blogModel.py
from webapp import db
from datetime import datetime
import bleach
from webapp.main._function import delete_blog_imgs


class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(256), index=True)
    body = db.Column(db.Text())
    timestamp = db.Column(db.DateTime, default=datetime.utcnow(), index=True)
    body_html = db.Column(db.Text())
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    looks = db.Column(db.BigInteger, default=0)

    comments = db.relationship('Comment', backref='blog', lazy='dynamic')
    imgs = db.relationship('BlogImgs', backref='blog', lazy='dynamic')

    # 每浏览一次，浏览量自动加一
    def ping(self):
        self.looks += 1
        db.session.add(self)

    #删除博客
    def delete_blog(self):
        for c in self.comments:
            db.session.delete(c)
        delete_blog_imgs(self)
        db.session.delete(self)

    # 将博客内容自动生成html格式
    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        # 允许的标签
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',\
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'img', 'span']
        # 允许的标签属性
        allowed_columns = {
            '*': ['class', 'id', 'style', 'background', 'title', 'width', 'height'],
            'a': ['href', 'rel'],
            'img': ['src', 'alt'],
        }
        target.body_html = bleach.clean(value, tags=allowed_tags, attributes=allowed_columns, strip=True)


db.event.listen(Blog.body, 'set', Blog.on_changed_body)
