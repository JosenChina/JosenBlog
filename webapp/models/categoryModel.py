# _*_ coding: utf-8 _*_
# filename: categoryModel.py
from webapp import db
from datetime import datetime


registrations = db.Table('registrations',
                         db.Column('category_id', db.Integer, db.ForeignKey('categorys.id')),
                         db.Column('blog_id', db.Integer, db.ForeignKey('blogs.id'))
                         )


class Category(db.Model):
    __tablename__ = 'categorys'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())

    blogs = db.relationship('Blog',
                            secondary=registrations,
                            backref=db.backref('categorys', lazy='dynamic'),
                            lazy='dynamic')

