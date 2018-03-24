# _*_ coding: utf-8 _*_
# filename: blogImgsModel.py

from webapp import db


class BlogImgs(db.Model):
    __tablename__ = 'blog_imgs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    img_url = db.Column(db.Text)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))

    # 删除（不提交）
    def delete_img_from_imgs(self):
        db.session.delete(self)
