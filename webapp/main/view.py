# _*_ coding: utf-8 _*_
# filename: view.py
from . import _main
from flask import render_template


@_main.route('/')
def index():


    return render_template('main/index.html')