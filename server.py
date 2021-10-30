# http://pac-api.timfang.xyz:10002/
from flask import Flask, request, Response,render_template
import hashlib
import json
import flask
import time
from werkzeug.utils import redirect
import cs_user
import cs_encrypt

print(cs_user.api_user_login(
    "MC13735292967@163.com", "cfa61b8570f11587c8774066f4cfad0a9d4e1f31f29d8a2b8aea26fc59a2b829110c72be2aa96fc4c74b69a0d0bf1c08be3b3fb50605db2192a3bc08e8f5c04b"))
print(cs_user.user_online("uck"))

app = Flask(__name__)

config={"siteName":"CloudStudy"}


@app.route('/')
def index():
    return(render_template('index.html',config=config,title="首页"))


@app.route('/login')
def login():
    return (render_template('login/index.html',config=config,title="登录"))


@app.route('/register')
def register():
    return (render_template('register/index.html', config=config, title="注册"))


@app.route('/admin')
def admin():
    return (render_template('admin/index.html', config=config, title="仪表盘"))


@app.route('/api')
def api():
    return redirect("/")


@app.route('/api/login')
def api_login():
    email = request.headers.get('cs_email')
    pwd = request.headers.get('cs_password')
    return cs_user.api_user_login(email,pwd)

@app.route('/api/register')
def api_register():
    name = request.headers.get('cs_name')
    email = request.headers.get('cs_email')
    pwd = request.headers.get('cs_password')
    return cs_user.api_user_register(name,email,pwd)

@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Method"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response


if __name__ == "__main__":
    app.run(debug=True, port=11451, host="0.0.0.0")
