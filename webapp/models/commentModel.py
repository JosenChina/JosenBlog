# _*_ coding: utf-8 _*_
# filename: commentModel.py
from webapp import db
from datetime import datetime


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text())
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    disabled = db.Column(db.Boolean, default=False)

    reports = db.relationship('CommentReport', backref='comment', lazy='dynamic')

    def __repr__(self):
        return '<Comment %r>' % self.id

    # 屏蔽该评论
    def disabling(self):
        self.disabled = True
        db.session.add(self)
        db.session.commit()

    # 评论（添加一行）
    def add_one(self):
        db.session.add(self)
        db.session.commit()

    # 删除一条评论
    def delete_one(self):
        db.session.delete(self)
        db.session.commit()

    # 删除一条评论不提交（提升删除多条的运行速度）
    def delete_one_from_manay(self):
        db.session.delete(self)

    # 开启评论
    def enable_comment(self):
        self.disabled = False
        db.session.add(self)
        db.session.commit()

    # 禁用评论
    def disable_comment(self):
        self.disabled = True
        db.session.add(self)
        db.session.commit()

    #