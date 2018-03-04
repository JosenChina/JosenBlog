# _*_ coding: utf-8 _*_
# filename: __init__.py
# about: 百度编辑器
from flask import Blueprint
from flask_login import current_user
from webapp.upload_file_qcloud_cos import cos_class
from time import time

_ueditor = Blueprint('ueditor', __name__)

CONFIG = dict(
    imageActionName='uploadimage',
    imageFieldName="upfile",  # 提交的图片表单名称
    imageMaxSize=2048000,  # 上传大小限制,单位B
    imageAllowFiles=['.png', '.PNG', '.jpg', '.JPG', '.jpeg',
                     '.JPEG', '.gif', '.GIF', '.bmp', '.BMP'],  # 上传图片格式显示
    imageCompressEnable=True,  # 是否压缩图片,默认是true
    imageCompressBorder=1600,  # 图片压缩最长边限制
    imageInsertAlign="none",  # 插入的图片浮动方式
    imageUrlPrefix="",  # 图片访问路径前缀
    imagePathFormat="upload/{yyyy}/{mm}/{dd}/{time}{rand:6}"    # 上传保存路径,可以自定义保存路径和文件名格式
    # {filename} 会替换成原文件名,配置这项需要注意中文乱码问题
    # /* {rand:6} 会替换成随机数,后面的数字是随机数的位数 */
    # /* {time} 会替换成时间戳 */
    # /* {yyyy} 会替换成四位年份 */
    # /* {yy} 会替换成两位年份 */
    # /* {mm} 会替换成两位月份 */
    # /* {dd} 会替换成两位日期 */
    # /* {hh} 会替换成两位小时 */
    # /* {ii} 会替换成两位分钟 */
    # /* {ss} 会替换成两位秒 */
    # /* 非法字符 \ : * ? " < > | */
    # /* 具请体看线上文档: fex.baidu.com/ueditor/#use-format_upload_filename */
)


def upload_image(file_body, blog_id):
    '''上传图片'''
    img_name = str(time()).replace('.', '')
    file_name = '/users/%s/blog_img/%s/%s.jpg'\
                % (current_user.username, blog_id, img_name)
    cos_class.upload_file(file_body, file_name)
    return {
        "state": "SUCCESS",
        "url":  cos_class.cos_path + file_name,
        "title": img_name + ".jpg",
        "original": img_name + ".jpg"
    }


from .view import *