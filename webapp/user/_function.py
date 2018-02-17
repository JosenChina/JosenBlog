# _*_ coding: utf-8 _*_
# filename: _function.py
from webapp.upload_file_qcloud_cos import cos_class
import os


class ChangeAvatar:
    # 检查图片格式是否合法
    @staticmethod
    def if_file_name(file_name):
        allow_name = ['JPG', 'jpg', 'JPEG', 'jpeg', 'PNG', 'png', 'GIF', 'gif']
        return '.' in file_name and file_name.rsplit('.', 1)[1] in allow_name

    @staticmethod
    def change_avatar(file_body, username):
        # 修改头像
        # 其中file_body为文件流，file_name为文件上传位置“/”隔开会自动上传到对应的文件夹，若没有对应的文件夹则会自动创建对应的文件夹
        file_name = '/users/%s/avatar.jpg' % username
        # cos_class.delete_file(file_name)
        cos_class.upload_file(file_body, file_name)

    @staticmethod
    def get_avatar_hash(username):
        return 'http://%s-%s.cosgz.myqcloud.com/users/%s/avatar.jpg' %\
               (os.environ.get('cos_bucket'), os.environ.get('cos_app_id'), username)