# _*_ coding: utf-8 _*_
# filename: commentReportsModel.py
from webapp import db
from datetime import datetime


class CommentReport(db.Model):
    __tablename__ = 'comment_reports'
    id = db.Column(db.Integer, db.ForeignKey('comments.id'), primary_key=True, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    instruction = db.Column(db.String(128))

    def __repr__(self):
        return '<CommentReport %d>' % self.id

    # 添加行
    def add_one(self):
        db.session.add(self)
        db.session.commit()

    # 删除行
    def delete_one(self):
        db.session.delete(self)
        db.session.commit()

    # 刷新
    def ping(self):
        self.timestamp = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

