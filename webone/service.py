from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import url_for
from models import User
from models import Question
from models import Comment
from models import Project
from models import HttpApi
from models import HttpCase

from exts import db


def login_service():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        phone = request.form.get('phone')
        password = request.form.get('password')
        user = User.query.filter(User.phone == phone).first()
        if not user:
            return '手机未注册、请先进行注册'
        else:
            if password == user.password:
                # 添加session 保持登陆状态
                session['user_id'] = user.id
                # 如果向在31天内无需在登陆、设置如下
                session.permanent = True
                return redirect(url_for('index'))
            else:
                return "手机号、或密码错误、请重新输入"


def register_service():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        phone = request.form.get('phone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # 手机号码验证、如果注册过就不能注册
        user = User.query.filter(User.phone == phone).first()
        if user:
            return '该手机号吗已经被注册、请检查'
        else:
            # 检查两次密码输入是否相同、相同才可以注册
            if password1 != password2:
                return "两次密码输入不一致、请重新输入"
            else:
                user = User(phone=phone, username=username, password=password1, )
                db.session.add(user)
                db.session.commit()
                # 注册成功、页面跳转到登陆页面
                return redirect(url_for('login'))


def question_service():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        print("提交问答成功、、、、")
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title, content=content)
        # 获取当前登陆的用户的信息
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question.user = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))


def detail_service(question_id):
    question_detail = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html', question_detail=question_detail)


def add_comment_service():
    content = request.form.get('content')
    question_id = request.form.get('question_id')
    user_id = session['user_id']
    comment = Comment(content=content, user_id=user_id)
    user = User.query.filter(User.id == user_id).first()
    question = Question.query.filter(Question.id == question_id).first()
    comment.author = user
    comment.question = question
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('detail', question_id=question_id))


def project_service():
    if request.method == 'GET':
        content = {
            "projects": Project.query.order_by('create_time').all()
        }
        return render_template('project.html', **content)
    else:
        name = request.form.get('name')
        description = request.form.get('description')
        project = Project(name=name, description=description)
        # 获取当前登陆的用户的信息
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        project.user = user
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('project'))


def project_remove_service(project_id):
    project = Project.query.filter(Project.id == project_id).first()
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('project'))


def http_api_service():
    if request.method == 'GET':

        content = {
            "projects": Project.query.order_by('create_time').all(),
            "apis": HttpApi.query.all()
        }
        return render_template('httpApi.html', **content)
    else:
        project_id = request.form.get('project')
        project2 = Project.query.filter(Project.id == project_id).first()
        name = request.form.get('name')
        method = request.form.get('method')
        path = request.form.get('path')
        body = request.form.get('body')
        header = request.form.get('header')
        content_type = request.form.get('contentType')
        http_api2 = HttpApi(name=name, method=method, path=path, body=body, header=header, contentType=content_type,
                            project=project2)
        user_id = session['user_id']
        user = User.query.filter(User.id == user_id).first()
        http_api2.user = user
        db.session.add(http_api2)
        db.session.commit()
        return redirect(url_for('http_api'))


def project_api_service(project_id):
    if request.method == 'GET':

        content = {
            "projects": [Project.query.filter(Project.id == project_id).first()],
            "apis": HttpApi.query.filter(HttpApi.project_id == project_id).all()
        }
        return render_template('httpApi.html', **content)
    else:
        user_id = session['user_id']
        print("当前用户的编号"+str(user_id))
        project_id = request.form.get('project')
        project2 = Project.query.filter(Project.id == project_id).first()
        name = request.form.get('name')
        method = request.form.get('method')
        path = request.form.get('path')
        body = request.form.get('body')
        header = request.form.get('header')
        content_type = request.form.get('contentType')
        http_api2 = HttpApi(name=name, method=method, path=path, body=body, header=header, contentType=content_type,
                            project=project2)
        user = User.query.filter(User.id == user_id).first()
        http_api2.user = user
        db.session.add(http_api2)
        db.session.commit()
        return redirect(url_for('project_api', project_id=project_id))


def remove_api_service(http_api_id):
    http_api = HttpApi.query.filter(HttpApi.id == http_api_id).first()
    db.session.delete(http_api)
    db.session.commit()
    return redirect(url_for('http_api'))


def http_case_service():
    if request.method == 'GET':
        content = {
            "projects": Project.query.order_by('create_time').all(),
            "apis": HttpApi.query.all(),
            "cases": HttpCase.query.all()
        }
        return render_template('httpCase.html', **content)
    else:
        print(request.form)
        case_name = request.form.get('case_name')
        project_id = request.form.get('project')
        http_api_id = request.form.get('http_api_id')
        body = request.form.get('body')
        http_api = HttpApi.query.filter(HttpApi.id == http_api_id).first()
        project = Project.query.filter(Project.id == project_id).first()

        http_case = HttpCase(case_name=case_name)
        http_case.body = body
        http_case.api_name = http_api.name
        http_case.api_id = http_api.id
        http_case.method = http_api.method
        http_case.path = http_api.path
        http_case.contentType = http_api.contentType
        http_case.header = http_api.header
        http_case.body = http_api.body
        http_case.project = project
        http_case.project_id = project_id
        user_id = session['user_id']
        http_case.user_id = user_id
        user = User.query.filter(User.id == user_id).first()
        http_case.user = user
        db.session.add(http_case)
        db.session.commit()
        return redirect('http_case')


def http_case_one_service(project_id):
    if request.method == 'GET':
        content = {
            "projects": Project.query.filter(Project.id == project_id).order_by('create_time').all(),
            "apis": HttpApi.query.filter(HttpApi.project_id == project_id).all(),
            "cases": HttpCase.query.filter(HttpCase.project_id == project_id).all()
        }
        print(content)
        return render_template('httpCase.html', **content)
    else:
        pass

