# _*_ coding: utf-8 _*_
# filename: JosenBlog.py
import os
from webapp import create_app

app = create_app(os.environ.get('FLASKY_CONFIG') or 'default')

if __name__ == '__main__':
    app.run()
