from flask import Flask
from flask import render_template
from flask import redirect
from flask import session
from flask import url_for
from flask import request
from models import User
from models import Question
from models import Project
from models import HttpApi
from models import HttpCase

from service import login_service
from service import register_service
from service import question_service
from service import detail_service
from service import add_comment_service
from service import project_service
from service import project_remove_service
from service import http_api_service
from service import remove_api_service
from service import project_api_service
from service import http_case_service
from service import http_case_one_service

import config
import requests
from exts import db
from decorators import login_required

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    """
        首页内容
    """
    content = {'questions': Question.query.order_by('create_time').all(), }
    return render_template('index.html', **content)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """
        登陆功能
    """
    return login_service()


@app.route('/logout')
def logout():
    """
        退出登陆
    """
    # session.pop('user_id')
    # del session['user_id']
    session.clear()
    return redirect(url_for('login'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    """
        注册功能
    """
    return register_service()


@app.route('/question', methods=['GET', 'POST'])
@login_required
def question():
    """
        问答社区功能
    """
    return question_service()


@app.route('/detail/<question_id>')
@login_required
def detail(question_id):
    """
    问答详情页面
    """
    return detail_service(question_id)


@app.route('/add_comment', methods=["POST"])
@login_required
def add_comment():
    """
    添加评论
    """
    return add_comment_service()


@app.context_processor
def my_context_process():
    """
    上下文处理
    """
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    return {}


@app.route('/project', methods=['GET', 'POST'])
@login_required
def project():
    """
    GET、显示项目列表页面
    POST、添加新项目
    """
    return project_service()


@app.route('/project_remove/<project_id>', methods=['GET'])
@login_required
def remove_project(project_id):
    """
    删除项目
    """
    return project_remove_service(project_id)


@app.route('/http_api/', methods=['GET', 'POST'])
@login_required
def http_api():
    """
    接口展示、添加业务
    """
    return http_api_service()


@app.route('/remove_api/<http_api_id>', methods=['GET'])
@login_required
def remove_api(http_api_id):
    """
    删除接口
    """
    return remove_api_service(http_api_id)


@app.route("/http_case/", methods=['GET', 'POST'])
@login_required
def http_case():
    """
        接口测试用例
    """
    return http_case_service()


@app.route("/http_case_one/<project_id>", methods=['GET', 'POST'])
@login_required
def http_case_one(project_id):
    """
    指定唯一项目情况下返回单个项目的测试用例
    """
    return http_case_one_service(project_id)


@app.route("/http_suite")
@login_required
def http_suite():
    return render_template('httpSuite.html')


@app.route("/http_suite_one")
@login_required
def http_suite_one():
    pass


@app.route("/getman")
@login_required
def getman():
    return render_template('getman.html')


@app.route('/project_api/<project_id>', methods=['GET', 'POST'])
@login_required
def project_api(project_id):
    """
    返回指特定项目的接口信息、根据项目id
    """
    return project_api_service(project_id)


@app.route("/run/case/<case_id>")
@login_required
def run_case(case_id):
    """
    执行测试用例
    """
    case = HttpCase.query.filter(HttpCase.id == case_id).first()
    data = {
        'method': case.method,
        'path': case.path,
        'data': case.body.encode('utf-8')
    }
    print(data)
    res = requests.request(method=data['method'], url=data['path'], data=data['data'])
    print(res.content)
    case.status = 1
    db.session.add(case)
    db.session.commit()
    return redirect('http_case')


@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'GET':
        return render_template('temp.html')
    else:
        print(request.form)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5005', debug=True)
