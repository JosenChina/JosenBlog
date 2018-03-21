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