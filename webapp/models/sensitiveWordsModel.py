# _*_ coding: utf-8 _*_
# filename: sensitiveWordsModel
from webapp import db
from datetime import datetime


class SensitiveWord(db.Model):
    __tables__ = 'sensitive_words'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    word = db.Column(db.String(128), index=True, unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<word %r>' % self.word

    # 刷新
    def ping(self):
        self.timestamp = datetime.utcnow()

    # 插入一行
    def add_one(self):
        db.session.add(self)
        db.session.commit()

    # 删除一行
    def delete_one(self):
        db.session.delete(self)
        db.session.commit()
