# _*_ coding: utf-8 _*_
# filename: form.py
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from webapp.models.sensitiveWordsModel import SensitiveWord
import re


class CommentForm(FlaskForm):
    body = TextAreaField('评论内容', validators=[DataRequired('评论内容不能为空！')])
    submit = SubmitField('评论')

    def validate_body(self, field):
        senWo = {x.word in field.data for x in SensitiveWord.query.all()}
        if senWo & {1} == {1}:
            raise ValidationError('评论内容包含敏感词，请检查并重新输入！！！')