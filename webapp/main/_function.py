# _*_ coding: utf-8 _*_
# filename: _function.py

from webapp.upload_file_qcloud_cos import cos_class
from flask_login import current_user
from webapp import db


def delete_blog_imgs(blog):
    for i in blog.imgs:
        cos_class.delete_file(i.img_url)
        db.session.delete(i)
    cos_class.delete_file('/users/%s/blog_img/%s/' % (current_user.username, blog.id))



