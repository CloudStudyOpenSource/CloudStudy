# http://pac-api.timfang.xyz:11451/
import os

from flask import Flask, render_template, request
from werkzeug.utils import redirect

from modules import cs_user

app = Flask(__name__)

config = {"siteName": "CloudStudy"}

# views


@app.route('/')
def index():
    return(render_template('index.html', config=config, title="首页", requireLogin=False))


@app.route('/login')
def login():
    return (render_template('login/index.html', config=config, title="登录", requireLogin=False))


@app.route('/register')
def register():
    return (render_template('register/index.html', config=config, title="注册", requireLogin=False))


@app.route('/dashbroad')
def dashbroad():
    token = request.cookies.get("cs_token")
    user = cs_user.getUserData(token)
    if(user[0] == "success"):
        user = user[1][0]
    else:
        user = None
    return (render_template('dashbroad/index.html', config=config, title="面板", user=user))


@app.route('/admin')
def admin():
    return (render_template('admin/index.html', config=config, title="仪表盘"))


@app.route('/admin/config')
def admin_config():
    return (render_template('admin/config/index.html', config=config, title="仪表盘_参数设置"))


@app.route('/admin/user')
def admin_user():
    return (render_template('admin/user/index.html', config=config, title="仪表盘_用户"))


@app.route('/admin/exam')
def admin_exam():
    return (render_template('admin/exam/index.html', config=config, title="仪表盘_考试"))


@app.route('/admin/exam/new')
def admin_exam_new():
    return (render_template('admin/exam/new/index.html'))

# api


@app.route('/api')
def api():
    return redirect("/")


@app.route('/api/login')
def api_login():
    email = request.headers.get('cs_email')
    pwd = request.headers.get('cs_password')
    return cs_user.api_user_login(email, pwd)


@app.route('/api/register')
def api_register():
    name = request.headers.get('cs_name')
    email = request.headers.get('cs_email')
    pwd = request.headers.get('cs_password')
    return cs_user.api_user_register(name, email, pwd)


@app.route('/api/checklogin')
def api_checklogin():
    token = request.cookies.get("cs_token")
    return cs_user.api_user_checkLogin(token)


@app.route('/api/getUser')
def api_getUser():
    token = request.cookies.get("cs_token")
    return cs_user.api_get_user_data(token)


@app.route('/api/admin/getuser')
def api_admin_getuser():
    return cs_user.api_user_getlist()


@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Method"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Server"] = "You Guess?"
    temp_resp = response
    try:
        if(response.is_json == True):
            response.data = response.data.decode("unicode-escape")
            response.headers["Cache-Control"] = "no-cache, must-revalidate"
    except:
        response = temp_resp
        print("JSON format error")
    return response


if __name__ == "__main__":
    app.run(debug=True, port=11451, host="0.0.0.0")
