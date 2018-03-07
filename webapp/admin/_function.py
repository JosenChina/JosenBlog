# _*_ coding: utf-8 _*_
# filename: _function.py
from wtforms import TextAreaField, SubmitField
import bleach

# 允许的标签
allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',\
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span']
# 允许的标签属性
allowed_columns = {
            '*': ['class', 'id', 'style', 'background', 'title', 'width', 'height'],
            'a': ['href', 'rel'],
        }


def clean(body):
    return bleach.linkify(bleach.clean(body, tags=allowed_tags, attributes=allowed_columns))