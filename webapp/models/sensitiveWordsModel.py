# _*_ coding: utf-8 _*_
# filename: sensitiveWordsModel
from webapp import db
from datetime import datetime
from config import basedir


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

    # 添加敏感词
    #
    @staticmethod
    def add_sensitive_words():
        with open(basedir+'/webapp/static/sensitiveWords.txt', 'r') as f:
            for word in f:
                # 当sensitiveWords.txt文件是Windows下创建时
                # SW = SensitiveWord.query.filter_by(word=unicode(word[:-2])).first() \
                #      or SensitiveWord(word=unicode(word[:-2]))

                # 当sensitiveWords.txt文件不是Windows下创建时
                SW = SensitiveWord.query.filter_by(word=unicode(word[:-1])).first() \
                     or SensitiveWord(word=unicode(word[:-1]))
                db.session.add(SW)
            db.session.commit()

    # 删除所有敏感词
    #
    @staticmethod
    def delete_all_words():
        for word in SensitiveWord.query.all():
            db.session.delete(word)
        db.session.commit()
