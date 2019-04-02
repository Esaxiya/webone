from exts import db
from datetime import datetime


class User(db.Model):
    """
    用户模型
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(11), nullable=False, )
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Question(db.Model):
    """
    问答模型
    """
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # now() 服务器第一次运行的时间、now是每次创建模型的时间
    create_time = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('question'))


class Comment(db.Model):
    """
    评论模型
    """
    __talbename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    # now() 服务器第一次运行的时间、now是每次创建模型的时间
    create_time = db.Column(db.DateTime, default=datetime.now)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question = db.relationship('Question', backref=db.backref('comments'))
    user = db.relationship('User', backref=db.backref('comments'))


class Project(db.Model):
    """
    项目模型
    """
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('projects'))


class HttpApi(db.Model):
    """
    http api 接口模型
    """
    __tablename__ = 'httpapi'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    path = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=True)
    header = db.Column(db.String(50), nullable=True)
    contentType = db.Column(db.String(100), nullable=False)
    # now() 服务器第一次运行的时间、now是每次创建模型的时间
    create_time = db.Column(db.DateTime, default=datetime.now)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    project = db.relationship('Project', backref=db.backref('apis'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('apis'))


class HttpCase(db.Model):
    """
    http case 模型
    """
    __tablename__ = 'httpcase'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    case_name = db.Column(db.String(50), nullable=False)
    api_name = db.Column(db.String(50), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    path = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=True)
    header = db.Column(db.Text, nullable=True)
    contentType = db.Column(db.String(500), nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0, comment="执行状态:0未执行;1执行成功;2执行失败")
    # now() 服务器第一次运行的时间、now是每次创建模型的时间
    create_time = db.Column(db.DateTime, default=datetime.now)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    project = db.relationship('Project', backref=db.backref('cases'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('cases'))
    api_id = db.Column(db.Integer, db.ForeignKey('httpapi.id'))
    httpApi = db.relationship('HttpApi', backref=db.backref('cases'))

#
