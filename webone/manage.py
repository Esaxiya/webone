from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app
from exts import db
from models import User
from models import Question
from models import Comment
from models import HttpApi

# from exts __import__(db)
# import sys <==>sys = __import__('sys')

manager = Manager(app)

# 使用Migrate绑定app和db
migrate = Migrate(app, db)

# 添加迁移脚本的命令到manger中
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
