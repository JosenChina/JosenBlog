# _*_ coding: utf-8 _*_
# filename: manage.py
import os
from webapp import db, create_app
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from webapp.models import *

app = create_app(os.environ.get('FLASKY_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()