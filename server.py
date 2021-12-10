# http://pac-api.timfang.xyz:11451/
# coding=utf-8
import os

from flask import Flask, render_template, request
from flask.json import jsonify
from werkzeug.utils import redirect

from modules import cs_user, cs_sql, cs_exam

app = Flask(__name__)

config = {"siteName": "CloudStudy"}


# 连接数据库
cs_sql.connectMysql()


# home


@app.route('/')
def index():
    if(cs_user.api_get_user_object(request.cookies.get("cs_token"))):
        return(redirect("/dashbroad"))
    else:
        return(render_template(
            'index.html',
            config=config,
            title="首页",
            requireLogin=False,
            user=cs_user.api_get_user_object(request.cookies.get("cs_token"))
        ))


# auth


@ app.route('/login')
def login():
    return (render_template(
        'login/index.html',
        config=config,
        title="登录",
        requireLogin=False,
        user=cs_user.api_get_user_object(request.cookies.get("cs_token"))
    ))


@ app.route('/register')
def register():
    return (render_template(
        'register/index.html',
        config=config,
        title="注册",
        requireLogin=False,
        user=cs_user.api_get_user_object(request.cookies.get("cs_token"))
    ))


# dashbroad


@ app.route('/dashbroad')
def dashbroad():
    return (render_template(
        'dashbroad/index.html',
        config=config,
        title="面板",
        user=cs_user.api_get_user_object(request.cookies.get("cs_token"))
    ))


# user


@ app.route('/user/settings')
def user_settings():
    return (render_template(
        'user/settings/index.html',
        config=config,
        title="用户设置",
        user=cs_user.api_get_user_object(request.cookies.get("cs_token"))
    ))


# admin


@ app.route('/admin')
def admin():
    return (render_template(
        'admin/index.html',
        config=config,
        title="仪表盘",
        user=cs_user.api_get_user_object(request.cookies.get("cs_token"))
    ))


@ app.route('/admin/config')
def admin_config():
    return (render_template(
        'admin/config/index.html',
        config=config,
        title="仪表盘_参数设置",
        user=cs_user.api_get_user_object(request.cookies.get("cs_token"))
    ))


@ app.route('/admin/group')
def admin_group():
    return (render_template(
        'admin/group/index.html',
        config=config,
        title="仪表盘_分组",
        user=cs_user.api_get_user_object(request.cookies.get("cs_token")),
        userList=cs_user.api_user_getlist()
    ))


@ app.route('/admin/user')
def admin_user():
    return (render_template(
        'admin/user/index.html',
        config=config,
        title="仪表盘_用户",
        user=cs_user.api_get_user_object(request.cookies.get("cs_token")),
        userList=cs_user.api_user_getlist()
    ))


@ app.route('/admin/user/table')
def admin_user_table():
    return (render_template(
        'admin/user/table.html',
        userList=cs_user.api_user_getlist()
    ))


@ app.route('/admin/exam')
def admin_exam():
    return (render_template(
        'admin/exam/index.html',
        config=config,
        title="仪表盘_考试",
        user=cs_user.api_get_user_object(request.cookies.get("cs_token")),
        groupList=cs_user.api_group_getlist(),
        examList=cs_exam.api_exam_getlist()
    ))


@ app.route('/admin/exam/new')
def admin_exam_new():
    return (render_template(
        'admin/exam/new/index.html',
        groupList=cs_user.api_group_getlist(),
        user=cs_user.api_get_user_object(request.cookies.get("cs_token"))
    ))


# api


@ app.route('/api')
def api():
    return redirect("/")


@ app.route('/api/login')
def api_login():
    email = request.headers.get('cs_email')
    pwd = request.headers.get('cs_password')
    return cs_user.api_user_login(email, pwd)


@ app.route('/api/register')
def api_register():
    name = request.headers.get('cs_name')
    email = request.headers.get('cs_email')
    pwd = request.headers.get('cs_password')
    return cs_user.api_user_register(name, email, pwd)


@ app.route('/api/checklogin')
def api_checklogin():
    token = request.cookies.get("cs_token")
    return cs_user.api_user_checkLogin(token)


@ app.route('/api/user/settings/get')
def api_user_settings_get():
    token = request.cookies.get("cs_token")
    return cs_user.api_get_user_data(token)


@ app.route('/api/user/settings/upload')
def api_user_settings_upload():
    token = request.cookies.get("cs_token")
    data = request.args.get("data")
    return cs_user.api_upload_user_data(token, data)


@ app.after_request
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
