# _*_ coding: utf-8 _*_
# filename: view.py
from . import _ueditor, upload_image, CONFIG
from flask import request, session, make_response
from flask_login import login_required
import json


@_ueditor.route('/upload', methods=['GET', 'POST', 'OPTIONS'])
@login_required
def handle():
    action = request.args.get('action')
    if not action:
        result = {'state': '表单错误！'}
    if action == 'config':
        result = CONFIG
    elif action == 'uploadimage':
        result = upload_image(request.files[CONFIG.get('imageFieldName')], session.get('blog_id'))
        session['blog_avatar'] = session.get('blog_avatar') or result['url']
    else:
        result = {'state': '功能未实现！'}
    res = make_response(json.dumps(result))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Headers'] = 'X-Requested-With,X_Requested_With'
    return res
