# _*_ coding: utf-8 _*_
# filename: categoryModel.py
from webapp import db
from datetime import datetime
from .blogModel import Blog


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

    # 添加分类
    def add_one(self):
        db.session.add(self)
        db.session.commit()

    # 删除分类
    def delete_one(self):
        db.session.delete(self)
        db.session.commit()

    # 修改分类名称
    def change_name(self, name):
        self.name = name
        self.timestamp = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    # 为分类插入博客
    def add_blog(self, blog):
        if blog not in self.blogs.all():
            self.blogs.append(blog)
        else:
            print('hello')
        db.session.add(self)
        db.session.commit()

    # 为分类移除博客
    def remove_blog(self, blog):
        self.blogs.remove(blog)
        db.session.add(self)
        db.session.commit()
