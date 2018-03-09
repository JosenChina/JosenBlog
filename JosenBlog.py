# _*_ coding: utf-8 _*_
# filename: JosenBlog.py
import os
from webapp import create_app
from flask import redirect, url_for

app = create_app(os.environ.get('FLASKY_CONFIG') or 'default')


@app.route('/')
def Index():
    return redirect(url_for('main.index'))


if __name__ == '__main__':
    app.run()
