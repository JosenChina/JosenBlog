# _*_ coding: utf-8 _*_
# filename: form.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, DataRequired


class SenForm(FlaskForm):
    body = StringField('敏感词：', validators=[Length(max=128, message='长度不要超过128位！'), DataRequired('请输入敏感词！')])
    submit = SubmitField('添加')


