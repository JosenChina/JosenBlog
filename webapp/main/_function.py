# _*_ coding: utf-8 _*_
# filename: _function.py

from webapp.models import SensitiveWord


def check_sensitive(body):
    senWo = {x.word in body for x in SensitiveWord.query.all()}
    if senWo & {1} == {1}:
        raise Exception('评论内容包含敏感词，请检查并重新输入！！！')


