# _*_ coding: utf-8 _*_
# filename: form.py
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    body = TextAreaField('评论内容', validators=[DataRequired('评论内容不能为空！')])
    submit = SubmitField('评论')